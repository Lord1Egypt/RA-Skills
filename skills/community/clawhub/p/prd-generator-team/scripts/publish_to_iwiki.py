#!/usr/bin/env python3
"""
iWiki 一键发布脚本 v1.2 — PRD Generator Skill 专用

将 PRD 文档（md + 截图）自动打包为 zip → 上传到 iWiki → 调整图片显示尺寸，一条命令完成。

v1.2 变更：
  - adjust_image_sizes 支持 B端/C端差异化宽度：C端截图 width=375, B端截图 width=100%
  - 新增 load_pc_pages_from_flowmap() 从 flowmap-config.json 识别 PC端页面
  - 新增 is_pc_page() 综合判断（flowmap viewport + alt关键词匹配）

用法:
  python publish_to_iwiki.py <项目目录> <父页面ID> [选项]

参数:
  项目目录       PRD项目根目录（包含 {项目名}-prd.md 和 prototype/screenshots/）
  父页面ID       iWiki 目标父页面 ID

选项:
  --cover        覆盖同名文档（默认不覆盖）
  --no-cover     不覆盖同名文档（默认行为）
  --skip-resize  跳过图片尺寸调整（仅上传）
  --dry-run      仅打包和检查，不实际上传

示例:
  python publish_to_iwiki.py /data/workspace/.codebuddy/docs/prd/pet-diary 4018325353
  python publish_to_iwiki.py /data/workspace/.codebuddy/docs/prd/pet-diary 4018325353 --cover
  python publish_to_iwiki.py /data/workspace/.codebuddy/docs/prd/pet-diary 4018325353 --dry-run
"""

import os
import sys
import re
import glob
import json
import shutil
import zipfile
import tempfile
import io

# 确保 stdout/stderr 使用 UTF-8 编码
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# 导入同目录下的 connect_mcp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from connect_mcp import MCPClient


# ── 配置 ──────────────────────────────────────────────
FLOW_MAP_KEYWORDS = ['page-flow-map', '整体页面流程图', '流程全景图']
IMG_DISPLAY_WIDTH_MOBILE = "375"
IMG_DISPLAY_WIDTH_PC = "100%"
# B端页面识别关键词（admin前缀 或 flowmap-config中viewport=1440的页面）
PC_PAGE_KEYWORDS = ['admin', 'dashboard', 'management', 'backend', 'console', 'cms']
# ──────────────────────────────────────────────────────


def log(msg, level="INFO"):
    icons = {"INFO": "ℹ️", "OK": "✅", "WARN": "⚠️", "ERR": "❌", "STEP": "📌"}
    print(f"{icons.get(level, 'ℹ️')} {msg}")


def find_prd_md(project_dir):
    """在项目目录中找到 *-prd.md 文件"""
    pattern = os.path.join(project_dir, "*-prd.md")
    matches = glob.glob(pattern)
    if not matches:
        # 回退：任意 .md 文件（排除 qa-report）
        for f in glob.glob(os.path.join(project_dir, "*.md")):
            if "qa-report" not in f:
                matches.append(f)
    if not matches:
        return None
    return matches[0]


def find_screenshots(project_dir):
    """查找截图目录中的 png 文件"""
    screenshots_dir = os.path.join(project_dir, "prototype", "screenshots")
    if not os.path.isdir(screenshots_dir):
        return [], screenshots_dir
    pngs = glob.glob(os.path.join(screenshots_dir, "*.png"))
    return pngs, screenshots_dir


def run_checkpoint(md_path, images_dir):
    """
    执行 Step 7.1 CHECKPOINT — 打包前合规性检查
    返回 (passed: bool, errors: list[str])
    """
    errors = []

    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. 禁止 HTML <img> 标签
    if re.search(r'<img\b', content, re.IGNORECASE):
        errors.append("MD 文件中包含 HTML <img> 标签（zip 导入不识别，需改为 markdown ![](images/xx.png) 语法）")

    # 2. 禁止 base64 图片
    if 'data:image' in content:
        errors.append("MD 文件中包含 base64 图片（iWiki 无法处理）")

    # 3. 无占位符残留
    if 'SCREENSHOT_PLACEHOLDER' in content:
        errors.append("MD 文件中残留 SCREENSHOT_PLACEHOLDER 占位符")

    # 4. 无 AI 注释残留
    if 'AI_INSTRUCTION' in content:
        errors.append("MD 文件中残留 AI_INSTRUCTION 注释")

    # 5. images/ 目录存在且非空
    if not os.path.isdir(images_dir):
        errors.append(f"images/ 目录不存在: {images_dir}")
    else:
        image_files = [f for f in os.listdir(images_dir) if f.lower().endswith('.png')]
        if not image_files:
            errors.append("images/ 目录为空（无 png 文件）")
        else:
            # 6. 交叉校验：md 引用 vs 文件
            md_refs = set(re.findall(r'!\[[^\]]*\]\(images/([^)]+)\)', content))
            file_set = set(image_files)

            missing_files = md_refs - file_set
            if missing_files:
                errors.append(f"MD 中引用了但 images/ 目录缺少的文件: {missing_files}")

            orphan_files = file_set - md_refs
            if orphan_files:
                # 只是 warning，不阻塞
                log(f"images/ 中有未被 MD 引用的文件（不影响发布）: {orphan_files}", "WARN")

    return len(errors) == 0, errors


def create_zip(md_path, images_dir, output_zip_path):
    """
    打包 md + images/ 为 zip
    zip 内部结构：
      {名称}.md
      images/xxx.png
      images/yyy.png
    """
    md_filename = os.path.basename(md_path)

    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # 写入 md 文件
        zf.write(md_path, md_filename)

        # 写入 images/ 目录下所有 png
        if os.path.isdir(images_dir):
            for fname in os.listdir(images_dir):
                if fname.lower().endswith('.png'):
                    fpath = os.path.join(images_dir, fname)
                    zf.write(fpath, f"images/{fname}")

    return output_zip_path


def verify_zip(zip_path):
    """验证 zip 内容结构"""
    with zipfile.ZipFile(zip_path, 'r') as zf:
        names = zf.namelist()

    md_files = [n for n in names if n.endswith('.md')]
    img_files = [n for n in names if n.startswith('images/') and n.endswith('.png')]

    log(f"ZIP 内容: {len(md_files)} 个 md 文件, {len(img_files)} 张图片")
    for n in names:
        log(f"  - {n}")

    if not md_files:
        return False, "ZIP 内无 .md 文件"
    if not img_files:
        return False, "ZIP 内无 images/*.png 文件"

    return True, "ZIP 结构正确"


def upload_zip(client, zip_path, parent_id, cover=False):
    """上传 zip 到 iWiki，支持最多3次重试 + 指数退避"""
    file_size_mb = os.path.getsize(zip_path) / 1024 / 1024
    log(f"上传 ZIP: {zip_path} ({file_size_mb:.2f}MB)", "STEP")
    log(f"  父页面ID: {parent_id}")
    log(f"  覆盖模式: {'是' if cover else '否（安全模式）'}")

    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            result = client.upload_file(
                file_path=zip_path,
                parent_id=int(parent_id),
                task_type="md_import",
                cover=cover,
            )
            return result
        except Exception as e:
            if attempt < max_retries:
                wait_time = 2 ** (attempt - 1)  # 1s, 2s
                log(f"上传失败（第{attempt}次），{wait_time}秒后重试: {e}", "WARN")
                import time
                time.sleep(wait_time)
            else:
                log(f"上传失败（已重试{max_retries}次）: {e}", "ERR")
                return {'success': False, 'msg': f'上传失败（重试{max_retries}次后仍失败）: {e}'}


def load_pc_pages_from_flowmap(project_dir):
    """
    从 flowmap-config.json 读取 viewport=1440 的页面列表，
    返回 set of page names（小写，用于匹配 alt 文本）。
    """
    config_file = os.path.join(project_dir, 'flowmap-config.json')
    if not os.path.isfile(config_file):
        return set()
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        pc_pages = set()
        for node in config.get('nodes', []):
            vp = node.get('viewport')
            if vp and int(vp) >= 1440:
                node_id = node.get('id', '')
                label = node.get('label', '')
                if node_id:
                    pc_pages.add(node_id.lower())
                if label:
                    pc_pages.add(label.lower())
        return pc_pages
    except (json.JSONDecodeError, ValueError, KeyError):
        return set()


def is_pc_page(alt_text, pc_pages_from_flowmap):
    """
    判断一张截图是否属于B端/PC端页面：
    1. alt 文本匹配 flowmap-config 中 viewport=1440 的页面
    2. alt 文本包含 PC_PAGE_KEYWORDS 中的关键词
    """
    alt_lower = alt_text.lower()
    # 匹配 flowmap-config 中的 PC 页面
    for page_name in pc_pages_from_flowmap:
        if page_name in alt_lower:
            return True
    # 匹配关键词
    for kw in PC_PAGE_KEYWORDS:
        if kw in alt_lower:
            return True
    return False


def adjust_image_sizes(client, doc_id, project_dir=None):
    """
    调整 iWiki 文档中的图片显示尺寸（V1.2 — 支持B端/C端差异化宽度）
    - C端页面截图: ![name](url) → <img src="url" alt="name" width="375">
    - B端/PC端截图: ![name](url) → <img src="url" alt="name" width="100%">
    - 流程图: 保持原始宽度不限制
    
    返回 (success: bool, message: str)
    """
    doc_id_int = int(doc_id)

    # 加载 flowmap-config 中的 PC 页面列表（用于识别B端截图）
    pc_pages = set()
    if project_dir:
        pc_pages = load_pc_pages_from_flowmap(project_dir)
        if pc_pages:
            log(f"从 flowmap-config 识别到 {len(pc_pages)} 个PC端页面: {pc_pages}")

    # Step 1: 获取文档内容
    log("获取文档内容 (getDocument)...", "STEP")
    resp = client.call_tool('getDocument', {'docid': str(doc_id_int)})

    body = None
    if 'result' in resp and 'content' in resp['result']:
        for item in resp['result']['content']:
            if item.get('type') == 'text':
                text = item.get('text', '')
                try:
                    data = json.loads(text)
                    body = data.get('body', text)
                except (json.JSONDecodeError, AttributeError):
                    body = text
                break

    if not body:
        return False, "无法获取文档内容"

    # Step 2: 获取文档标题（saveDocument 必填）
    log("获取文档元数据 (metadata)...", "STEP")
    meta_resp = client.call_tool('metadata', {'docid': str(doc_id_int)})
    title = None
    if 'result' in meta_resp and 'content' in meta_resp['result']:
        for item in meta_resp['result']['content']:
            if item.get('type') == 'text':
                text = item.get('text', '')
                try:
                    data = json.loads(text)
                    title = data.get('title', '')
                except (json.JSONDecodeError, AttributeError):
                    pass
                break
    if not title:
        title = f"prd-doc-{doc_id_int}"
        log(f"未获取到标题，使用默认: {title}", "WARN")

    # Step 3: 替换图片引用（区分C端/B端/流程图）
    pattern = r'!\[([^\]]*)\]\((/tencent/api/attachments/s3/url\?attachmentid=(\d+))\)'

    mobile_count = 0
    pc_count = 0
    skip_count = 0

    def replacer(match):
        nonlocal mobile_count, pc_count, skip_count
        alt, url, att_id = match.group(1), match.group(2), match.group(3)
        # 流程图保持原样
        if any(kw in alt for kw in FLOW_MAP_KEYWORDS):
            skip_count += 1
            log(f"  [保持] 流程图: {alt}")
            return match.group(0)
        # 判断是否为PC端/B端截图
        if is_pc_page(alt, pc_pages):
            pc_count += 1
            log(f"  [调整] B端截图: {alt} → width={IMG_DISPLAY_WIDTH_PC}")
            return f'<img src="{url}" alt="{alt}" width="{IMG_DISPLAY_WIDTH_PC}">'
        # 默认为C端移动端截图
        mobile_count += 1
        log(f"  [调整] C端截图: {alt} → width={IMG_DISPLAY_WIDTH_MOBILE}")
        return f'<img src="{url}" alt="{alt}" width="{IMG_DISPLAY_WIDTH_MOBILE}">'

    new_body = re.sub(pattern, replacer, body)

    total_replaced = mobile_count + pc_count
    if total_replaced == 0 and skip_count == 0:
        log("文档中未找到 iWiki 内部图片引用，可能导入尚未完成", "WARN")
        return False, "未找到图片引用"

    log(f"替换统计: {mobile_count} 张C端截图(width={IMG_DISPLAY_WIDTH_MOBILE}), "
        f"{pc_count} 张B端截图(width={IMG_DISPLAY_WIDTH_PC}), "
        f"{skip_count} 张流程图保持原样")

    # Step 4: 保存文档
    log("保存文档 (saveDocument)...", "STEP")
    save_resp = client.call_tool('saveDocument', {
        'docid': doc_id_int,  # 必须是数字！
        'title': title,
        'body': new_body,
        'contenttype': 'MD'
    })

    if 'error' in save_resp:
        return False, f"保存失败: {save_resp['error']}"

    # Step 5: 二次验证
    log("二次验证 (getDocument)...", "STEP")
    verify_resp = client.call_tool('getDocument', {'docid': str(doc_id_int)})
    verify_body = None
    if 'result' in verify_resp and 'content' in verify_resp['result']:
        for item in verify_resp['result']['content']:
            if item.get('type') == 'text':
                text = item.get('text', '')
                try:
                    data = json.loads(text)
                    verify_body = data.get('body', text)
                except (json.JSONDecodeError, AttributeError):
                    verify_body = text
                break

    if verify_body:
        width_mobile = len(re.findall(rf'width="{IMG_DISPLAY_WIDTH_MOBILE}"', verify_body))
        width_pc = len(re.findall(rf'width="{IMG_DISPLAY_WIDTH_PC}"', verify_body))
        remaining_md_imgs = len(re.findall(pattern, verify_body))
        # remaining_md_imgs 中应该只有流程图
        flow_remaining = 0
        for m in re.finditer(pattern, verify_body):
            alt = m.group(1)
            if any(kw in alt for kw in FLOW_MAP_KEYWORDS):
                flow_remaining += 1

        non_flow_remaining = remaining_md_imgs - flow_remaining
        if non_flow_remaining > 0:
            log(f"仍有 {non_flow_remaining} 张页面截图未替换为 img 标签！", "WARN")
            return False, f"二次验证失败: {non_flow_remaining} 张截图未替换"

        log(f"二次验证通过: {width_mobile} 张C端(375), {width_pc} 张B端(100%), {flow_remaining} 张流程图保持原样", "OK")
    else:
        log("二次验证: 无法获取文档内容，跳过", "WARN")

    return True, f"成功调整 {total_replaced} 张图片尺寸（C端{mobile_count}张, B端{pc_count}张）"


def extract_doc_id_from_upload_result(result):
    """从上传结果中提取新创建的文档ID"""
    if not result:
        return None

    data = result.get('data', {})

    # 处理数组格式：[{pageid: xxx, status: 'finish', ...}]
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                for key in ['pageid', 'docid', 'doc_id', 'pageId', 'page_id', 'id']:
                    if key in item:
                        return item[key]

    # 处理字典格式
    if isinstance(data, dict):
        # 尝试常见字段
        for key in ['pageid', 'docid', 'doc_id', 'pageId', 'page_id', 'id']:
            if key in data:
                return data[key]
        # 递归查找
        for v in data.values():
            if isinstance(v, dict):
                for key in ['pageid', 'docid', 'doc_id', 'pageId', 'page_id', 'id']:
                    if key in v:
                        return v[key]

    # 从 msg 中提取
    msg = result.get('msg', '')
    match = re.search(r'(\d{8,})', str(msg))
    if match:
        return int(match.group(1))

    return None


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="PRD iWiki 一键发布：自动打包 zip + 上传 + 图片尺寸调整",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('project_dir', help='PRD 项目目录路径')
    parser.add_argument('parent_id', nargs='?', default=None,
                        help='iWiki 父页面 ID（--doc-id 模式下可省略）')
    parser.add_argument('--cover', action='store_true', default=False,
                        help='覆盖同名文档（默认不覆盖）')
    parser.add_argument('--no-cover', action='store_true', default=False,
                        help='不覆盖同名文档（默认行为）')
    parser.add_argument('--skip-resize', action='store_true', default=False,
                        help='跳过图片尺寸调整')
    parser.add_argument('--dry-run', action='store_true', default=False,
                        help='仅打包和检查，不实际上传')
    parser.add_argument('--doc-id', default=None,
                        help='已有文档ID（用于仅执行尺寸调整，跳过打包上传）')

    args = parser.parse_args()

    # O8: parent_id 条件必填 — --doc-id 模式下可省略
    if not args.doc_id and not args.parent_id:
        parser.error("parent_id 是必填参数（--doc-id 模式下可省略）")

    # --no-cover 优先级高于 --cover
    cover = args.cover and not args.no_cover

    project_dir = os.path.abspath(args.project_dir)

    print("=" * 60)
    print("🚀 PRD iWiki 一键发布")
    print("=" * 60)

    # ── 0. 环境检查 ──
    token = os.environ.get('TAI_PAT_TOKEN')
    if not token and not args.dry_run:
        log("未设置 TAI_PAT_TOKEN 环境变量", "ERR")
        log("请执行: export TAI_PAT_TOKEN=\"你的token\"")
        sys.exit(1)

    if not os.path.isdir(project_dir):
        log(f"项目目录不存在: {project_dir}", "ERR")
        sys.exit(1)

    # ── 仅尺寸调整模式 ──
    if args.doc_id:
        log(f"仅执行图片尺寸调整，文档ID: {args.doc_id}", "STEP")
        client = MCPClient(token=token)
        client.initialize()
        success, msg = adjust_image_sizes(client, args.doc_id, project_dir=project_dir)
        if success:
            log(msg, "OK")
            log(f"iWiki 页面: https://iwiki.woa.com/p/{args.doc_id}", "OK")
        else:
            log(msg, "ERR")
            sys.exit(1)
        return

    # ── 1. 查找 PRD 文件 ──
    log("Step 1: 查找 PRD 文件", "STEP")
    md_path = find_prd_md(project_dir)
    if not md_path:
        log(f"项目目录中未找到 *-prd.md 文件: {project_dir}", "ERR")
        sys.exit(1)
    log(f"PRD 文件: {md_path}", "OK")

    # ── 2. 查找截图 ──
    log("Step 2: 查找截图文件", "STEP")
    screenshots, screenshots_dir = find_screenshots(project_dir)
    if not screenshots:
        log(f"截图目录为空或不存在: {screenshots_dir}", "ERR")
        sys.exit(1)
    log(f"找到 {len(screenshots)} 张截图", "OK")

    # ── 3. 准备临时打包目录 ──
    log("Step 3: 准备打包", "STEP")
    project_name = os.path.basename(project_dir)
    tmp_dir = os.path.join(project_dir, f"{project_name}-zip-tmp")

    # 清理旧临时目录
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.makedirs(tmp_dir)

    images_dir = os.path.join(tmp_dir, "images")
    os.makedirs(images_dir)

    # 复制 md 文件
    tmp_md_path = os.path.join(tmp_dir, os.path.basename(md_path))
    shutil.copy2(md_path, tmp_md_path)

    # 复制所有截图到 images/
    for src in screenshots:
        dst = os.path.join(images_dir, os.path.basename(src))
        shutil.copy2(src, dst)

    copied_count = len(os.listdir(images_dir))
    log(f"已复制 {copied_count} 张截图到 images/", "OK")

    # ── 4. CHECKPOINT 检查 ──
    log("Step 4: CHECKPOINT 打包前检查", "STEP")
    passed, errors = run_checkpoint(tmp_md_path, images_dir)
    if not passed:
        for e in errors:
            log(e, "ERR")
        log("CHECKPOINT 未通过，中止发布", "ERR")
        # 清理
        shutil.rmtree(tmp_dir)
        sys.exit(1)
    log("CHECKPOINT 全部通过", "OK")

    # ── 5. 打包 ZIP ──
    log("Step 5: 打包 ZIP", "STEP")
    zip_path = os.path.join(project_dir, f"{project_name}-prd.zip")
    create_zip(tmp_md_path, images_dir, zip_path)

    # 验证 zip
    valid, msg = verify_zip(zip_path)
    if not valid:
        log(f"ZIP 验证失败: {msg}", "ERR")
        shutil.rmtree(tmp_dir)
        sys.exit(1)
    log(f"ZIP 打包完成: {zip_path}", "OK")

    # 清理临时目录
    shutil.rmtree(tmp_dir)

    if args.dry_run:
        log("dry-run 模式，跳过上传", "WARN")
        zip_size_mb = os.path.getsize(zip_path) / 1024 / 1024
        log(f"ZIP 文件: {zip_path} ({zip_size_mb:.2f}MB)", "OK")
        print("\n✅ Dry-run 完成！ZIP 已生成，可手动上传。")
        return

    # ── 6. 上传到 iWiki ──
    log("Step 6: 上传到 iWiki", "STEP")
    client = MCPClient(token=token)
    result = upload_zip(client, zip_path, args.parent_id, cover=cover)

    if not result.get('success'):
        log(f"上传失败: {result.get('msg', '未知错误')}", "ERR")
        if result.get('data'):
            log(f"详情: {json.dumps(result['data'], ensure_ascii=False)}")
        sys.exit(1)

    log("上传成功!", "OK")
    if result.get('data'):
        log(f"返回数据: {json.dumps(result['data'], indent=2, ensure_ascii=False)}")

    # 提取新文档 ID
    doc_id = extract_doc_id_from_upload_result(result)

    # ── 7. 图片尺寸调整 ──
    if not args.skip_resize:
        if doc_id:
            log(f"Step 7: 图片尺寸调整 (docid={doc_id})", "STEP")
            client.initialize()
            success, msg = adjust_image_sizes(client, doc_id, project_dir=project_dir)
            if success:
                log(msg, "OK")
            else:
                log(f"尺寸调整失败: {msg}", "WARN")
                log("可稍后手动执行: python publish_to_iwiki.py <项目目录> <父页面ID> --doc-id <文档ID>")
        else:
            log("未从上传结果中提取到文档ID，跳过尺寸调整", "WARN")
            log("请手动执行: python publish_to_iwiki.py <项目目录> <父页面ID> --doc-id <文档ID>")

    # ── 完成 ──
    print("\n" + "=" * 60)
    log("PRD 已发布到 iWiki!", "OK")
    if doc_id:
        log(f"iWiki 页面: https://iwiki.woa.com/p/{doc_id}", "OK")
    log(f"本地文件: {project_dir}", "OK")
    log(f"ZIP 包: {zip_path}", "OK")
    print("=" * 60)


if __name__ == "__main__":
    main()
