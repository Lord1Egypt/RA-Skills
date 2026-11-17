#!/usr/bin/env python3
"""
ICS 国家标准更新检查脚本（通用版）
从 openstd.samr.gov.cn 获取指定 ICS 分类的现行国家标准列表，
与本地已下载的标准清单进行比对，找出新增、删除和状态变更的标准。

用法:
  python3 check_updates.py --ics-code 35 --dir /path/to/standards
  python3 check_updates.py --ics-code 35 --dir /path/to/standards --download

环境变量（优先级低于命令行参数）:
  ICS_MONITOR_DIR     工作目录（存放 PDF 和元数据）
"""

import urllib.parse, urllib.request, re, json, os, time, sys, argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# ============ 命令行参数 ============

def parse_args():
    p = argparse.ArgumentParser(description='ICS 国家标准更新检查')
    p.add_argument('--ics-code', type=str, default=None,
                   help='ICS 分类代码（如 35），不指定则从环境变量 ICS_MONITOR_CODE 读取')
    p.add_argument('--dir', type=str, default=None,
                   help='工作目录（存放 PDF 和元数据），不指定则从环境变量 ICS_MONITOR_DIR 读取')
    p.add_argument('--download', action='store_true',
                   help='检查后自动下载新增标准')
    return p.parse_args()

# ============ 全局配置 ============

OPENSTD_BASE = 'https://openstd.samr.gov.cn/bzgk/gb'
PAGE_SIZE = 50

def init_config():
    args = parse_args()

    ics_code = args.ics_code or os.environ.get('ICS_MONITOR_CODE')
    if not ics_code:
        print('[!] 请指定 --ics-code 参数或设置环境变量 ICS_MONITOR_CODE')
        sys.exit(1)

    base_dir = args.dir or os.environ.get('ICS_MONITOR_DIR')
    if not base_dir:
        base_dir = os.path.join(os.getcwd(), f'国家标准_ICS{ics_code}')

    if not os.path.exists(base_dir):
        os.makedirs(base_dir, exist_ok=True)
        print(f'[!] 工作目录不存在，已自动创建: {base_dir}')

    return {
        'ics_code': ics_code,
        'base_dir': base_dir,
        'meta_file': os.path.join(base_dir, 'standards_metadata.json'),
        'latest_check_file': os.path.join(base_dir, 'latest_check.json'),
        'report_file': os.path.join(base_dir, 'update_report.json'),
        'do_download': args.download,
    }

CONFIG = None

def get_config():
    global CONFIG
    if CONFIG is None:
        CONFIG = init_config()
    return CONFIG

# ============ 抓取搜索结果 ============

def fetch_search_page(page_no):
    """从 openstd 获取一页搜索结果"""
    cfg = get_config()
    params = {
        'p.p1': '0',
        'p.p90': 'circulation_date',
        'p.p91': 'desc',
        'p.p2': '',
        'p.p5': 'PUBLISHED',
        'p.p6': cfg['ics_code'],
        'page': str(page_no),
        'pageSize': str(PAGE_SIZE),
    }
    query = '&'.join(f'{k}={urllib.parse.quote(str(v))}' for k, v in params.items())
    url = f'{OPENSTD_BASE}/std_list?{query}'

    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept': 'text/html',
    })

    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                html = resp.read().decode('utf-8', errors='replace')

            rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html, re.DOTALL)
            entries = []
            for row in rows:
                if 'showInfo' not in row:
                    continue

                hcno_match = re.search(r"showInfo\('([A-F0-9]{32})'\)", row)
                if not hcno_match:
                    continue
                hcno = hcno_match.group(1)

                cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
                if len(cells) < 5:
                    continue

                code = re.sub(r'<[^>]+>', '', cells[1]).strip().replace('&nbsp;', ' ')
                title = re.sub(r'<[^>]+>', '', cells[4]).strip().replace('&nbsp;', ' ') if len(cells) > 4 else ''
                std_type = re.sub(r'<[^>]+>', '', cells[5]).strip() if len(cells) > 5 else ''
                status = re.sub(r'<[^>]+>', '', cells[6]).strip() if len(cells) > 6 else ''

                if code and code.startswith('GB'):
                    entries.append({
                        'code': code,
                        'title': title,
                        'hcno': hcno,
                        'type': std_type,
                        'status': status,
                    })

            if page_no == 1:
                total_match = re.search(r'(\d+)\s*/\s*(\d+)', html)
                total_pages = int(total_match.group(2)) if total_match else 70
                return entries, total_pages

            return entries, None
        except Exception as e:
            if attempt < 2:
                time.sleep(2)
            else:
                print(f'  第{page_no}页出错: {e}')
                return [], None

def fetch_all_standards():
    """获取所有现行标准（并行抓取）"""
    cfg = get_config()
    ics_code = cfg['ics_code']
    print(f'[1/4] 正在从 openstd.samr.gov.cn 获取 ICS {ics_code} 标准列表...')

    page1_entries, total_pages = fetch_search_page(1)
    print(f'  第1页: {len(page1_entries)} 条, 总页数: {total_pages}')

    all_results = list(page1_entries)

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(fetch_search_page, p): p for p in range(2, total_pages + 1)}
        for future in as_completed(futures):
            page_no = futures[future]
            try:
                results, _ = future.result()
                all_results.extend(results)
                if page_no % 20 == 0:
                    print(f'  已获取 {page_no}/{total_pages} 页, 累计 {len(all_results)} 条')
            except Exception as e:
                print(f'  第{page_no}页失败: {e}')

    # 按 hcno 去重
    seen = set()
    unique = []
    for r in all_results:
        h = r['hcno']
        if h not in seen:
            seen.add(h)
            unique.append(r)

    print(f'  总计: {len(all_results)} 条, 去重后: {len(unique)} 条')
    return unique

# ============ 加载本地数据 ============

def load_existing_metadata():
    """加载本地已下载标准元数据"""
    cfg = get_config()
    meta_file = cfg['meta_file']
    base_dir = cfg['base_dir']

    print('[2/4] 正在加载本地已下载标准清单...')

    if not os.path.exists(meta_file):
        print(f'  [!] 未找到元数据文件: {meta_file}')
        return []

    with open(meta_file, 'r') as f:
        data = json.load(f)

    print(f'  本地元数据: {len(data)} 条')

    # 统计下载状态
    downloaded = sum(1 for d in data if d.get('download_status') == 'success')
    captcha = sum(1 for d in data if 'CAPTCHA' in d.get('download_status', ''))
    error = sum(1 for d in data if 'error' in d.get('download_status', ''))

    print(f'  已下载: {downloaded} | 验证码拦截: {captcha} | 服务器错误: {error}')

    # 检查磁盘上的PDF文件
    pdf_files = [f for f in os.listdir(base_dir) if f.endswith('.pdf')]
    pdf_size = sum(os.path.getsize(os.path.join(base_dir, f)) for f in pdf_files)
    print(f'  磁盘PDF文件: {len(pdf_files)} 个, 总大小: {pdf_size / 1024 / 1024:.1f} MB')

    return data

def load_previous_check():
    """加载上次检查结果（如果有）"""
    cfg = get_config()
    if os.path.exists(cfg['latest_check_file']):
        with open(cfg['latest_check_file'], 'r') as f:
            data = json.load(f)
        check_time = data.get('check_time', 'unknown')
        std_count = len(data.get('standards', []))
        print(f'  上次检查时间: {check_time}, 当时标准数: {std_count}')
        return data
    print(f'  (首次运行，无上次检查记录)')
    return None

# ============ 比对逻辑 ============

def compare_standards(latest_standards, existing_metadata, previous_check):
    """比对网站最新标准与本地已下载数据"""
    print('[3/4] 正在比对标准列表...')

    # 构建 hcno 查找表
    latest_by_hcno = {s['hcno']: s for s in latest_standards}
    existing_by_hcno = {d['hcno']: d for d in existing_metadata if d.get('hcno')}

    # 按 code 构建查找表（用于交叉比对）
    existing_by_code = {}
    for d in existing_metadata:
        code = d.get('code', '')
        if code:
            existing_by_code.setdefault(code, []).append(d)

    # 1. 新增标准（网站有，本地无）
    new_standards = []
    for s in latest_standards:
        if s['hcno'] not in existing_by_hcno:
            new_standards.append(s)

    # 2. 已删除/废止标准（本地有，网站无）
    removed_standards = []
    for d in existing_metadata:
        hcno = d.get('hcno', '')
        if hcno and hcno not in latest_by_hcno:
            removed_standards.append({
                'hcno': hcno,
                'code': d.get('code', ''),
                'title': d.get('title', ''),
                'old_status': d.get('status', ''),
                'download_status': d.get('download_status', ''),
            })

    # 3. 状态变更
    status_changes = []
    for s in latest_standards:
        if s['hcno'] in existing_by_hcno:
            old = existing_by_hcno[s['hcno']]
            if old.get('status', '') != s['status']:
                status_changes.append({
                    'hcno': s['hcno'],
                    'code': s['code'],
                    'title': s['title'],
                    'old_status': old.get('status', ''),
                    'new_status': s['status'],
                })

    # 4. 标题变更
    title_changes = []
    for s in latest_standards:
        if s['hcno'] in existing_by_hcno:
            old = existing_by_hcno[s['hcno']]
            if old.get('title', '') != s['title']:
                title_changes.append({
                    'hcno': s['hcno'],
                    'code': s['code'],
                    'old_title': old.get('title', ''),
                    'new_title': s['title'],
                })

    # 5. 可重试下载的标准（之前下载失败但非404采标的标准，且网站仍为现行）
    retry_candidates = []
    for d in existing_metadata:
        if d.get('hcno') in latest_by_hcno:
            dl_status = d.get('download_status', '')
            should_retry = (
                ('CAPTCHA' in dl_status or 'error' in dl_status)
                and 'not_downloadable' not in dl_status
            )
            if should_retry:
                retry_candidates.append({
                    'hcno': d['hcno'],
                    'code': d.get('code', ''),
                    'title': d.get('title', ''),
                    'old_status': dl_status,
                })

    # 6. 与上次检查比对增量变化
    incremental_new = []
    incremental_removed = []
    if previous_check:
        prev_standards = previous_check.get('standards', [])
        prev_by_hcno = {s['hcno']: s for s in prev_standards}

        for s in prev_standards:
            if s['hcno'] not in latest_by_hcno:
                incremental_removed.append(s)

        for s in latest_standards:
            if s['hcno'] not in prev_by_hcno:
                incremental_new.append(s)

    report = {
        'check_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'website_total': len(latest_standards),
        'local_total': len(existing_metadata),
        'new_standards': new_standards,
        'removed_standards': removed_standards,
        'status_changes': status_changes,
        'title_changes': title_changes,
        'retry_candidates': retry_candidates,
        'incremental_new': incremental_new,
        'incremental_removed': incremental_removed,
        'summary': {
            'new_count': len(new_standards),
            'removed_count': len(removed_standards),
            'status_change_count': len(status_changes),
            'title_change_count': len(title_changes),
            'retry_candidate_count': len(retry_candidates),
            'incremental_new_count': len(incremental_new),
            'incremental_removed_count': len(incremental_removed),
        }
    }

    print(f'  新增标准: {len(new_standards)}')
    print(f'  已删除/废止: {len(removed_standards)}')
    print(f'  状态变更: {len(status_changes)}')
    print(f'  标题变更: {len(title_changes)}')
    print(f'  可重试下载(验证码/错误): {len(retry_candidates)}')
    if previous_check:
        print(f'  自上次检查新增: {len(incremental_new)}')
        print(f'  自上次检查删除: {len(incremental_removed)}')

    return report

# ============ 可选: 下载新增标准 ============

def download_new_standards(new_standards, batch_size=4, batch_pause=65):
    """下载新增标准PDF（批量策略：每batch_size个暂停batch_pause秒，避免触发验证码）

    经验教训：
    - 网站每5次下载请求后触发验证码，冷却约60秒重置
    - 404错误=采标标准（网站不提供全文下载），不是验证码问题
    - isValid=false 才是真正的验证码拦截
    """
    import http.cookiejar
    cfg = get_config()
    meta_file = cfg['meta_file']

    success = 0
    not_downloadable = 0  # 404采标标准
    captcha_hit = 0       # isValid=false 验证码拦截
    error = 0
    downloaded_records = []  # 用于更新元数据

    print(f'\n开始下载 {len(new_standards)} 个新增标准（批量策略: 每{batch_size}个暂停{batch_pause}秒）...')

    for i, std in enumerate(new_standards, 1):
        hcno = std['hcno']
        code = std['code']
        title = std['title']

        safe_code = re.sub(r'[/\\:*?"<>|]', '-', code).strip()
        safe_title = re.sub(r'[/\\:*?"<>|]', '-', title).strip()
        if len(safe_title) > 80:
            safe_title = safe_title[:80]
        filename = f'{safe_code}_{safe_title}.pdf'
        output_path = os.path.join(cfg['base_dir'], filename)

        # 断点续传：已存在则跳过
        if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
            success += 1
            downloaded_records.append({
                **std,
                'download_status': 'success',
                'download_file': filename,
                'download_size': os.path.getsize(output_path),
            })
            continue

        cookie_jar = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
        opener.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'),
            ('Accept', 'text/html,application/xhtml+xml,application/pdf,*/*'),
            ('Referer', 'https://openstd.samr.gov.cn/bzgk/gb/')
        ]

        show_url = f'{OPENSTD_BASE}/showGb?type=download&hcno={hcno}'
        try:
            resp = opener.open(show_url, timeout=15)
            show_html = resp.read().decode('utf-8', errors='replace')
        except urllib.error.HTTPError as e:
            if e.code == 404:
                not_downloadable += 1
                downloaded_records.append({**std, 'download_status': 'not_downloadable: 404'})
                print(f'  [{i}/{len(new_standards)}] {code}: 404 (采标标准，不可下载)')
            else:
                error += 1
                downloaded_records.append({**std, 'download_status': f'failed: http_{e.code}'})
                print(f'  [{i}/{len(new_standards)}] {code}: HTTP {e.code}')
            time.sleep(2)
            continue
        except Exception as e:
            error += 1
            downloaded_records.append({**std, 'download_status': f'failed: {type(e).__name__}'})
            print(f'  [{i}/{len(new_standards)}] {code}: {type(e).__name__}')
            time.sleep(2)
            continue

        is_valid_match = re.search(r"isValid\s*[:=]\s*['\"]?(true|false)['\"]?", show_html, re.IGNORECASE)
        is_valid = is_valid_match and is_valid_match.group(1).lower() == 'true'

        if not is_valid:
            captcha_hit += 1
            downloaded_records.append({**std, 'download_status': 'failed: CAPTCHA'})
            print(f'  [{i}/{len(new_standards)}] {code}: 验证码拦截，等{batch_pause}秒...')
            time.sleep(batch_pause)
            continue

        view_url = f'{OPENSTD_BASE}/viewGb?hcno={hcno}'
        try:
            resp = opener.open(view_url, timeout=30)
            pdf_data = resp.read()
            if len(pdf_data) > 1000 and pdf_data[:4] == b'%PDF':
                with open(output_path, 'wb') as f:
                    f.write(pdf_data)
                success += 1
                downloaded_records.append({
                    **std,
                    'download_status': 'success',
                    'download_file': filename,
                    'download_size': len(pdf_data),
                })
                print(f'  [{i}/{len(new_standards)}] {code}: ✓ 下载成功 ({len(pdf_data)} bytes)')
            elif len(pdf_data) == 0:
                not_downloadable += 1
                downloaded_records.append({**std, 'download_status': 'not_downloadable: not_pdf'})
                print(f'  [{i}/{len(new_standards)}] {code}: 空内容 (服务器资源缺失)')
            else:
                error += 1
                downloaded_records.append({**std, 'download_status': 'failed: not_pdf'})
                print(f'  [{i}/{len(new_standards)}] {code}: 非PDF内容 ({len(pdf_data)} bytes)')
        except Exception as e:
            error += 1
            downloaded_records.append({**std, 'download_status': f'failed: {type(e).__name__}'})
            print(f'  [{i}/{len(new_standards)}] {code}: 下载错误 {type(e).__name__}')

        # 批量暂停策略：每batch_size个暂停batch_pause秒
        if i % batch_size == 0 and i < len(new_standards):
            print(f'  ⏸ 批次暂停 {batch_pause}秒 (已完成 {i}/{len(new_standards)})...')
            time.sleep(batch_pause)
        else:
            time.sleep(2)

    print(f'\n下载完成: 成功 {success}, 采标(404) {not_downloadable}, 验证码 {captcha_hit}, 错误 {error}')

    # 更新元数据文件
    if downloaded_records:
        try:
            with open(meta_file, 'r') as f:
                existing_data = json.load(f)
            existing_hcnos = {d.get('hcno') for d in existing_data}
            for record in downloaded_records:
                if record['hcno'] not in existing_hcnos:
                    existing_data.append(record)
                    existing_hcnos.add(record['hcno'])
            with open(meta_file, 'w') as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=2)
            print(f'元数据已更新')
        except Exception as e:
            print(f'元数据更新失败: {e}')

    return success, not_downloadable, captcha_hit, error

# ============ 主函数 ============

def main():
    cfg = get_config()
    ics_code = cfg['ics_code']

    print('=' * 60)
    print(f'ICS {ics_code} 国家标准 - 更新检查')
    print(f'工作目录: {cfg["base_dir"]}')
    print(f'检查时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('=' * 60)

    # 1. 获取网站最新标准
    latest_standards = fetch_all_standards()

    # 2. 加载本地数据
    print()
    existing_metadata = load_existing_metadata()

    print()
    previous_check = load_previous_check()

    # 3. 比对
    print()
    report = compare_standards(latest_standards, existing_metadata, previous_check)

    # 保存最新检查数据
    latest_data = {
        'check_time': report['check_time'],
        'standards': latest_standards,
    }
    with open(cfg['latest_check_file'], 'w') as f:
        json.dump(latest_data, f, ensure_ascii=False)
    print(f'\n[4/4] 最新检查数据已保存')

    # 保存报告
    with open(cfg['report_file'], 'w') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f'更新报告已保存: {cfg["report_file"]}')

    # 可选: 下载新增标准
    if cfg['do_download'] and report['new_standards']:
        download_new_standards(report['new_standards'])

    # 打印摘要
    print('\n' + '=' * 60)
    print('检查结果摘要')
    print('=' * 60)
    print(f'网站现行标准总数: {report["website_total"]}')
    print(f'本地元数据总数:   {report["local_total"]}')
    print(f'新增标准:         {report["summary"]["new_count"]}')
    print(f'已删除/废止:      {report["summary"]["removed_count"]}')
    print(f'状态变更:         {report["summary"]["status_change_count"]}')
    print(f'可重试下载:       {report["summary"]["retry_candidate_count"]}')

    if report['new_standards']:
        print(f'\n--- 新增标准 (前20个) ---')
        for s in report['new_standards'][:20]:
            print(f'  {s["code"]} - {s["title"][:60]}')
        if len(report['new_standards']) > 20:
            print(f'  ...还有 {len(report["new_standards"]) - 20} 个')

    if report['status_changes']:
        print(f'\n--- 状态变更 (前10个) ---')
        for c in report['status_changes'][:10]:
            print(f'  {c["code"]}: {c["old_status"]} -> {c["new_status"]}')

    if report['removed_standards']:
        print(f'\n--- 已删除/废止标准 (前10个) ---')
        for r in report['removed_standards'][:10]:
            print(f'  {r["code"]} - {r["title"][:50]}')

    print('\n' + '=' * 60)
    if report['summary']['new_count'] > 0:
        print(f'共发现 {report["summary"]["new_count"]} 个新增标准!')
        if not cfg['do_download']:
            print(f'提示: 运行 python3 check_updates.py --ics-code {ics_code} --dir {cfg["base_dir"]} --download 可自动下载新增标准')
    else:
        print('暂无新增标准，所有标准均为已知。')
    print('=' * 60)

if __name__ == '__main__':
    main()
