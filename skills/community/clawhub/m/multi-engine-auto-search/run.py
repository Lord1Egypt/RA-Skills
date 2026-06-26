# -*- coding: utf-8 -*-
"""
multi-engine-auto-search - 全引擎自动聚合搜索
发现并并行调用所有已安装的搜索类技能脚本，聚合去重后输出
"""
import sys, json, subprocess, re, os, concurrent.futures
from collections import OrderedDict

OPENCLAW_SKILLS = r'C:\Users\86195\.openclaw\skills'
WORKSPACE_SKILLS = r'C:\Users\86195\.openclaw\workspace\skills'
TMP_FILE = os.path.join(os.environ.get('TEMP', '/tmp'), 'mes_result.json')

def curl_get(url, timeout=12):
    """直接用curl抓取（不依赖任何skill，独立可用）"""
    try:
        r = subprocess.run(
            ['curl.exe', '-s', '-L', '--max-time', str(timeout),
             '-H', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
             '-H', 'Accept-Language: zh-CN,zh;q=0.9', url],
            capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=timeout+3
        )
        return r.stdout
    except:
        return ''

def extract_bing(text):
    results = []
    for m in re.finditer(r'<li[^>]*class="b_algo[^"]*"[^>]*>.*?<h2[^>]*><a[^>]*href="([^"]+)"[^>]*>(.*?)</a>.*?<p[^>]*>(.*?)</p>', text, re.DOTALL|re.IGNORECASE):
        url = m.group(1).strip()
        title = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        snippet = re.sub(r'<[^>]+>', '', m.group(3)).strip()
        if url and title:
            results.append({'title': title, 'url': url, 'snippet': snippet[:200], 'source': 'Bing-Direct'})
    return results

def search_bing_direct(query, count=10):
    url = 'https://cn.bing.com/search?q=' + urllib_parse.quote(query) + '&count=' + str(count)
    return extract_bing(curl_get(url))

def discover_search_skills():
    """扫描所有skills目录，发现有搜索功能的脚本"""
    scripts = []
    seen = set()
    for base in [OPENCLAW_SKILLS, WORKSPACE_SKILLS]:
        if not os.path.exists(base):
            continue
        for name in os.listdir(base):
            skill_path = os.path.join(base, name)
            if not os.path.isdir(skill_path):
                continue
            key = name.lower()
            if key in seen:
                continue
            # 跳过非搜索类技能（除非是核心的多引擎）
            if not any(kw in key for kw in ['search', 'web', 'find', 'cn', 'browser']):
                continue
            seen.add(key)
            # 找脚本
            for script_name, stype in [('run.py', 'run'), ('scripts/search.py', 'searchpy')]:
                script_path = os.path.join(skill_path, script_name)
                if os.path.exists(script_path):
                    scripts.append({'name': name, 'path': script_path, 'type': stype, 'dir': skill_path})
                    break
    return scripts

def call_one_skill(sinfo, query):
    """调用单个搜索技能，返回结果列表"""
    path = sinfo['path']
    name = sinfo['name']
    stype = sinfo['type']

    # 写临时文件，传递查询词（解决中文编码问题）
    infile = os.path.join(os.environ.get('TEMP', '/tmp'), 'mes_in.json')
    with open(infile, 'w', encoding='utf-8') as f:
        json.dump({'query': query}, f)

    try:
        if stype == 'run':
            # 调用 run.py，传查询词
            result = subprocess.run(
                [sys.executable, path, query, '--json'],
                capture_output=True, text=True, timeout=20,
                encoding='utf-8', errors='replace'
            )
        else:
            # search.py 类型
            result = subprocess.run(
                [sys.executable, path, '--query', query, '--max-results', '8'],
                capture_output=True, text=True, timeout=20,
                encoding='utf-8', errors='replace'
            )

        # 从临时文件读取JSON结果（子进程写入的）
        if os.path.exists(TMP_FILE):
            try:
                with open(TMP_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                results = []
                for r in data.get('results', []):
                    if isinstance(r, dict) and r.get('url'):
                        results.append({
                            'title': r.get('title', ''),
                            'url': r.get('url', ''),
                            'snippet': r.get('snippet', ''),
                            'source': r.get('source', name)
                        })
                return results
            except:
                pass

        # 回退：解析stdout的JSON
        output = result.stdout.strip()
        if output.startswith('{') or output.startswith('['):
            try:
                data = json.loads(output)
                results = []
                for r in data.get('results', data if isinstance(data, list) else []):
                    if isinstance(r, dict) and r.get('url'):
                        results.append({
                            'title': r.get('title', ''),
                            'url': r.get('url', ''),
                            'snippet': r.get('snippet', ''),
                            'source': r.get('source', name)
                        })
                return results
            except:
                pass
        return []
    except subprocess.TimeoutExpired:
        return []
    except Exception:
        return []

def main():
    if len(sys.argv) < 2:
        print('Usage: run.py <keyword>')
        return

    query = sys.argv[1]
    print('')
    print('== [Multi-Engine Search] ' + query + ' ==')
    print('')

    # 1. 发现所有搜索技能
    skills = discover_search_skills()
    print('[Discovery] Found ' + str(len(skills)) + ' search skill(s):')
    for s in skills:
        print('  - ' + s['name'] + ' (' + s['type'] + ')')
    print('')

    # 2. 并行调用所有搜索技能
    all_results = OrderedDict()
    if skills:
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(skills)) as executor:
            futures = {executor.submit(call_one_skill, s, query): s['name'] for s in skills}
            for future in concurrent.futures.as_completed(futures):
                name = futures[future]
                try:
                    results = future.result()
                    print('[' + name + '] +' + str(len(results)))
                    for r in results:
                        url = r.get('url', '')
                        if url and url not in all_results:
                            all_results[url] = r
                except Exception as e:
                    print('[' + name + '] 0')
                    continue

    # 3. 如果没有任何结果，自动用Bing兜底
    if not all_results:
        print('[Fallback] Using Bing direct search...')
        bing_results = search_bing_direct(query, 10)
        for r in bing_results:
            url = r.get('url', '')
            if url and url not in all_results:
                all_results[url] = r

    results = list(all_results.values())
    if not results:
        print('[Failed] No results.')
        return

    # 4. 核心答案
    snippets = [r['snippet'] for r in results if r.get('snippet')]
    if snippets:
        print('')
        print('== [Core Answer] ==')
        seen = []
        for s in snippets:
            core = s[:200].strip().replace('&nbsp;', ' ').replace('&#183;', '·').replace('&ensp;', ' ')
            if core and core not in seen:
                print('  ' + core)
                seen.append(core)
                if len(seen) >= 4:
                    break
        print('')

    active_sources = ', '.join(sorted(set(r.get('source', '?') for r in results)))
    print('')
    print('== [Total: ' + str(len(results)) + ' unique | Sources: ' + active_sources + '] ==')
    for idx, r in enumerate(results[:15], 1):
        print('')
        print(str(idx) + '. [' + r.get('source', '?') + '] ' + r['title'])
        if r.get('snippet'):
            print('   ' + r['snippet'][:150])
        print('   ' + r['url'])

if __name__ == '__main__':
    import urllib.parse as urllib_parse
    main()
