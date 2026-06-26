"""
Markdown 到微信兼容 HTML 的转换器（独立版）

将 .md 格式的文章文件转换为经过微信内联样式适配的富文本 HTML。
此版本已从原项目解耦，不依赖 src.core.settings 等内部模块。
"""

import re
from pathlib import Path
from typing import Dict, Optional

import markdown

from html_formatter import HTMLFormatter


class MarkdownConverter:
    """Markdown 文件到微信兼容 HTML 的转换器"""

    # 微信图文正文内容的 UTF-8 字节上限
    MAX_CONTENT_BYTES = 2000000

    # 启用的 Markdown 扩展列表
    MD_EXTENSIONS = [
        'tables',
        'fenced_code',
        'toc',
        'sane_lists',
    ]

    @classmethod
    def convert_text(cls, raw_md: str, title: str = None, publisher=None,
                     md_path: Optional[Path] = None,
                     save_html: bool = False, save_dir: Optional[Path] = None,
                     save_filename: str = 'preview') -> Optional[Dict]:
        """
        转换 Markdown 纯文本字符串为微信兼容的文章字典

        Args:
            raw_md: Markdown 纯文本字符串
            title: 指定文章标题，若不传则自动从 Markdown 提取
            publisher: 可选的微信客户端实例，用于上传正文内嵌图片
            md_path: 原始文件路径（可选，若提供则可用于解析相对路径的图片）
            save_html: 是否将转换后的 HTML 保存到本地供预览
            save_dir: 本地预览保存目录（save_html=True 时使用）
            save_filename: 本地预览保存的文件名（不含后缀）
        """
        # 清理文件名中 Windows 不允许的特殊字符
        save_filename = re.sub(r'[<>:"/\\|?*]', '', save_filename).strip()

        # 解析 Front Matter 元数据块
        front_matter, raw_md = cls._parse_front_matter(raw_md)

        if not title:
            title = front_matter.get('title') or cls._extract_title(raw_md, save_filename)

        author = front_matter.get('author', '')
        summary = front_matter.get('summary') or cls._extract_summary(raw_md)
        publish_at = front_matter.get('publish_at', None)
        publish_mode = front_matter.get('publish_mode', 'draft')

        # 将从正文中提取到的第一行 # 标题移除，避免正文中重复出现标题
        raw_md = cls._remove_title_from_md(raw_md)

        # 调用 markdown 库转换为原始 HTML
        raw_html = cls._md_to_html(raw_md)

        # 补充表格的内联样式
        raw_html = cls._style_tables(raw_html)

        # 清理微信不兼容的特殊字符
        raw_html = cls._sanitize_for_wechat(raw_html)

        # 使用 HTMLFormatter 做微信内联样式适配
        wechat_html = HTMLFormatter.format_for_wechat(raw_html)

        # 处理正文内嵌图片：上传到微信并替换 src
        if publisher and md_path:
            wechat_html = cls._upload_and_replace_images(
                wechat_html, md_path.parent, publisher
            )

        # 检查并处理超长内容
        content_bytes = len(wechat_html.encode('utf-8'))
        if content_bytes > cls.MAX_CONTENT_BYTES:
            wechat_html = cls._truncate_content(wechat_html, cls.MAX_CONTENT_BYTES)
            new_bytes = len(wechat_html.encode('utf-8'))
            print(f"⚠️  文章内容过长 ({content_bytes} 字节)，已截断至 {new_bytes} 字节以符合微信限制")

        # 保存本地预览 HTML
        if save_html and save_dir:
            try:
                save_dir = Path(save_dir)
                save_dir.mkdir(parents=True, exist_ok=True)
                out_file = save_dir / f"{save_filename}.html"

                preview_html = (
                    f"<!DOCTYPE html>\n<html>\n<head>\n<meta charset='utf-8'>\n"
                    f"<meta name='viewport' content='width=device-width, initial-scale=1.0'>\n"
                    f"<title>{title} - 本地预览</title>\n"
                    f"<style>body {{ max-width: 677px; margin: 20px auto; padding: 20px; font-family: -apple-system, system-ui, sans-serif; background: #f7f7f7; }} "
                    f"#wechat-article {{ background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }}</style>\n"
                    f"</head>\n<body>\n<div id='wechat-article'>\n"
                    f"<h1 style='font-size: 22px; margin-bottom: 20px;'>{title}</h1>\n"
                    f"{wechat_html}\n"
                    f"</div>\n</body>\n</html>"
                )
                out_file.write_text(preview_html, encoding='utf-8')
                print(f"💾 转换结果已保存至本地预览: {out_file}")
            except Exception as e:
                print(f"⚠️  保存本地 HTML 预览失败: {e}")

        result = {
            'title': title,
            'content': wechat_html,
            'author': author,
            'summary': summary,
            'publish_at': publish_at,
            'publish_mode': publish_mode,
            'account_id': front_matter.get('account_id', 'default')
        }
        return result

    @classmethod
    def convert_file(cls, md_path: str, publisher=None, save_html: bool = False,
                     save_dir: Optional[Path] = None) -> Optional[Dict]:
        """
        读取 .md 文件并调用 convert_text 转换为微信兼容的文章字典

        Args:
            md_path: Markdown 文件的绝对或相对路径
            publisher: 可选的微信客户端实例，用于上传正文内嵌图片
            save_html: 是否保存本地预览 HTML
            save_dir: 本地预览保存目录

        Returns:
            包含 title, content, author, summary 的字典
        """
        md_path = Path(md_path)
        if not md_path.exists():
            print(f"❌ 文件不存在: {md_path}")
            return None

        try:
            raw_md = md_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"❌ 读取文件失败: {e}")
            return None

        result = cls.convert_text(
            raw_md=raw_md,
            publisher=publisher,
            md_path=md_path,
            save_html=save_html,
            save_dir=save_dir,
            save_filename=md_path.stem
        )

        return result

    @classmethod
    def _parse_front_matter(cls, md_text: str) -> tuple:
        """
        解析 Markdown 文件头部的 YAML Front Matter 元数据块

        支持的字段：title, author, summary, cover, publish_at, publish_mode, account_id
        """
        pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
        match = re.match(pattern, md_text.strip(), re.DOTALL)

        if not match:
            return {}, md_text

        yaml_block = match.group(1)
        body = match.group(2)

        meta = {}
        for line in yaml_block.splitlines():
            line = line.strip()
            if ':' in line:
                key, _, value = line.partition(':')
                key = key.strip().lower()
                value = value.strip().strip('"').strip("'")
                if key in ('title', 'author', 'summary', 'cover', 'publish_at', 'publish_mode', 'account_id'):
                    meta[key] = value

        if meta:
            fields = ', '.join(f'{k}={v}' for k, v in meta.items())
            print(f"📋 解析到 Front Matter 元数据: {fields}")

        return meta, body

    @classmethod
    def _md_to_html(cls, md_text: str) -> str:
        """使用 markdown 库将 Markdown 文本转换为 HTML"""
        html = markdown.markdown(
            md_text,
            extensions=cls.MD_EXTENSIONS,
            output_format='html5',
        )
        return html

    @classmethod
    def _extract_title(cls, md_text: str, fallback: str = '未命名文章') -> str:
        """从 Markdown 正文中提取标题（第一个 # 开头的行）"""
        for line in md_text.splitlines():
            line = line.strip()
            if line.startswith('# ') and not line.startswith('## '):
                return line.lstrip('# ').strip()
        return fallback

    @classmethod
    def _remove_title_from_md(cls, md_text: str) -> str:
        """从 Markdown 正文中剥去第一行 # 开头的标题"""
        lines = md_text.splitlines()
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('# ') and not stripped.startswith('## '):
                del lines[i]
                break
        return '\n'.join(lines)

    @classmethod
    def _extract_summary(cls, md_text: str, max_len: int = 120) -> str:
        """提取摘要：跳过标题和目录锚点后，取第一个有意义的段落"""
        in_code_block = False
        found_title = False

        for line in md_text.splitlines():
            stripped = line.strip()

            if stripped.startswith('```'):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue

            if stripped.startswith('#'):
                found_title = True
                continue

            if not stripped or stripped.startswith('- [') or stripped == '---':
                continue

            if found_title:
                clean = re.sub(r'[*_`\[\]()]', '', stripped)
                return clean[:max_len]

        return '暂无摘要'

    @classmethod
    def _style_tables(cls, html: str) -> str:
        """替换 markdown 库输出的裸 <table> 标签为带有内联样式的版本"""
        html = html.replace(
            '<table>',
            '<table style="border-collapse: collapse; width: 100%; margin: 1.5em 0; font-size: 14px;">'
        )
        html = html.replace(
            '<th>',
            '<th style="border: 1px solid #ddd; padding: 8px 12px; background-color: #f2f2f2; font-weight: bold; text-align: left;">'
        )
        html = html.replace(
            '<td>',
            '<td style="border: 1px solid #ddd; padding: 8px 12px;">'
        )
        return html

    @classmethod
    def _sanitize_for_wechat(cls, html: str) -> str:
        """
        清理微信 API 不兼容的特殊字符和 HTML 结构
        """
        # Box-Drawing 字符 → ASCII 替代
        box_replacements = {
            '┌': '+', '┐': '+', '└': '+', '┘': '+',
            '├': '+', '┤': '+', '┬': '+', '┴': '+', '┼': '+',
            '─': '-', '│': '|',
            '→': '->', '←': '<-', '↓': 'v', '↑': '^',
            '═': '=', '║': '|', '╔': '+', '╗': '+', '╚': '+', '╝': '+',
            '╠': '+', '╣': '+', '╦': '+', '╩': '+', '╬': '+',
            '▶': '>', '◀': '<', '▼': 'v', '▲': '^',
            '●': '*', '○': 'o', '◆': '*', '◇': 'o',
        }
        for old, new in box_replacements.items():
            html = html.replace(old, new)

        # 移除 codehilite 扩展产生的 <div> 包装层
        html = re.sub(r'<div[^>]*class="codehilite"[^>]*>', '', html)
        html = html.replace('</div>', '')

        # 清除 class 属性
        html = re.sub(r'\s+class="[^"]*"', '', html)

        # 清除 id 属性
        html = re.sub(r'\s+id="[^"]*"', '', html)

        # 修正自闭合标签格式
        html = re.sub(r'<(hr|br)\s*/?\s*>', r'<\1>', html)
        html = html.replace('<hr/>', '<hr>')
        html = html.replace('<br/>', '<br>')

        # 移除空的 <span></span> 标签
        html = re.sub(r'<span>\s*</span>', '', html)

        # 移除不可见控制字符（保留换行、回车、制表符）
        html = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', html)

        return html

    @classmethod
    def _upload_and_replace_images(cls, html: str, base_dir: Path, publisher) -> str:
        """
        检测 HTML 中的 <img> 标签，将本地图片上传到微信并替换 src 为微信 URL

        Args:
            html: 含有 <img> 标签的 HTML 字符串
            base_dir: Markdown 文件所在的目录
            publisher: 微信客户端实例（需要有 upload_content_image 方法）
        """
        img_pattern = re.compile(r'<img\s+[^>]*src="([^"]+)"[^>]*/?>',  re.IGNORECASE)
        matches = img_pattern.findall(html)

        if not matches:
            return html

        print(f"🖼️  检测到 {len(matches)} 张图片，正在上传到微信...")

        for local_src in matches:
            if local_src.startswith('http://') or local_src.startswith('https://'):
                continue

            image_path = base_dir / local_src
            if not image_path.exists():
                alt_path = base_dir.parent / base_dir.stem / local_src
                if alt_path.exists():
                    image_path = alt_path
                else:
                    print(f"   ⚠️  图片不存在: {local_src}")
                    continue

            wechat_url = publisher.upload_content_image(str(image_path))
            if wechat_url:
                old_img = f'src="{local_src}"'
                new_img = f'src="{wechat_url}"'
                html = html.replace(old_img, new_img)
                print(f"   ✅ {local_src} -> 微信 URL")
            else:
                print(f"   ❌ {local_src} 上传失败")

        # 给所有 <img> 标签添加微信兼容的内联样式
        html = re.sub(
            r'<img\s',
            '<img style="max-width: 100%; height: auto; display: block; margin: 1em auto;" ',
            html
        )

        return html

    @classmethod
    def _truncate_content(cls, html: str, max_bytes: int) -> str:
        """安全截断 HTML 内容（按 UTF-8 字节计量）"""
        notice = (
            '<hr style="border: none; border-top: 2px dashed #ccc; margin: 2em 0;">'
            '<p style="font-size: 16px; line-height: 1.75; color: #999; text-align: center;">'
            '⚠️ 本文内容较长，已截取前半部分。完整内容请查阅原文档。</p>'
        )
        notice_bytes = len(notice.encode('utf-8'))
        target_bytes = max_bytes - notice_bytes - 500

        estimated_chars = int(target_bytes / 1.5)
        truncated = html[:min(estimated_chars, len(html))]

        while len(truncated.encode('utf-8')) > target_bytes and len(truncated) > 100:
            truncated = truncated[:int(len(truncated) * 0.9)]

        last_close = -1
        for close_tag in ['</p>', '</pre>', '</table>', '</h2>', '</h3>', '</ul>', '</ol>', '</blockquote>']:
            pos = truncated.rfind(close_tag)
            if pos > last_close:
                last_close = pos + len(close_tag)

        if last_close > 0:
            truncated = truncated[:last_close]

        return truncated + notice
