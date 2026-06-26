#!/usr/bin/env python3
"""
飞书知识库文档写入器 - 发布版
支持 Markdown 解析、富文本、标题识别、图片插入
"""
import json
import urllib.request
import time
import os
import sys
import argparse
import re
import base64
from typing import Dict, List, Optional

class LarkWikiWriter:
    """飞书知识库文档写入器"""
    
    def __init__(self, app_id: str = None, app_secret: str = None, 
                 space_id: str = None, wiki_domain: str = None):
        """
        初始化飞书知识库写入器
        
        Args:
            app_id: 飞书应用 ID
            app_secret: 飞书应用密钥
            space_id: 知识库 Space ID
            wiki_domain: 飞书域名（如 your-domain.larksuite.com）
        """
        # 优先级：参数 > 环境变量
        self.app_id = app_id or os.environ.get('LARK_APP_ID')
        self.app_secret = app_secret or os.environ.get('LARK_APP_SECRET')
        self.space_id = space_id or os.environ.get('LARK_SPACE_ID')
        self.wiki_domain = wiki_domain or os.environ.get('LARK_WIKI_DOMAIN', 'your-domain.larksuite.com')
        self.base_url = "https://open.larksuite.com"
        self.access_token = None
        
        # 验证必需参数
        if not self.app_id:
            raise ValueError("缺少 LARK_APP_ID，请通过参数或环境变量提供")
        if not self.app_secret:
            raise ValueError("缺少 LARK_APP_SECRET，请通过参数或环境变量提供")
        if not self.space_id:
            raise ValueError("缺少 LARK_SPACE_ID，请通过参数或环境变量提供")
    
    def _get_token(self) -> str:
        """获取 access token"""
        url = f"{self.base_url}/open-apis/auth/v3/tenant_access_token/internal"
        data = json.dumps({
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }).encode('utf-8')
        
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read())
                if result.get('code') == 0:
                    self.access_token = result['tenant_access_token']
                    return self.access_token
                else:
                    # 友好的错误提示
                    code = result.get('code')
                    msg = result.get('msg', '未知错误')
                    if code == 99991663:
                        raise Exception("APP_ID 或 APP_SECRET 错误，请检查配置")
                    elif code == 99991664:
                        raise Exception("应用权限不足，请在飞书开放平台添加知识库权限")
                    else:
                        raise Exception(f"获取 token 失败: {msg} (code: {code})")
        except urllib.error.URLError as e:
            raise Exception(f"网络错误: {e}")
    
    def _ensure_token(self):
        """确保有有效的 token"""
        if not self.access_token:
            self._get_token()
    
    def create_document(self, title: str, parent_node_token: str = None) -> Dict:
        """
        创建文档
        
        Args:
            title: 文档标题
            parent_node_token: 父节点 token（可选）
        
        Returns:
            包含 node_token, obj_token, url 的字典
        """
        self._ensure_token()
        
        if not parent_node_token:
            parent_node_token = os.environ.get('LARK_PARENT_NODE')
            if not parent_node_token:
                raise ValueError("缺少 parent_node_token 参数或 LARK_PARENT_NODE 环境变量")
        
        url = f"{self.base_url}/open-apis/wiki/v2/spaces/{self.space_id}/nodes"
        data = json.dumps({
            "obj_type": "docx",
            "parent_node_token": parent_node_token,
            "node_type": "origin",
            "title": title
        }).encode('utf-8')
        
        req = urllib.request.Request(url, data=data, headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        })
        
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read())
                if result.get('code') == 0:
                    node = result['data']['node']
                    return {
                        'node_token': node['node_token'],
                        'obj_token': node['obj_token'],
                        'url': f"https://{self.wiki_domain}/wiki/{node['node_token']}"
                    }
                else:
                    raise Exception(f"创建文档失败: {result.get('msg', '未知错误')}")
        except urllib.error.URLError as e:
            raise Exception(f"网络错误: {e}")
    
    def _parse_markdown_to_blocks(self, content: str) -> List[Dict]:
        """将 Markdown 转换为飞书 blocks"""
        blocks = []
        lines = content.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # 跳过空行
            if not line.strip():
                i += 1
                continue
            
            # 标题处理
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if heading_match:
                level = len(heading_match.group(1))
                text = heading_match.group(2).strip()
                blocks.append(self._create_heading_block(level, text))
                i += 1
                continue
            
            # 分隔线
            if re.match(r'^---+$', line) or re.match(r'^\*\*\*+$', line):
                blocks.append({"block_type": 22, "divider": {}})
                i += 1
                continue
            
            # 无序列表
            if line.strip().startswith('- ') or line.strip().startswith('* '):
                text = line.strip()[2:]
                blocks.append(self._create_bullet_block(text))
                i += 1
                continue
            
            # 有序列表
            ordered_match = re.match(r'^\d+\.\s+(.+)$', line.strip())
            if ordered_match:
                text = ordered_match.group(1)
                blocks.append(self._create_ordered_block(text))
                i += 1
                continue
            
            # 代码块
            if line.strip().startswith('```'):
                code_lines = []
                lang = line.strip()[3:].strip()
                i += 1
                while i < len(lines) and not lines[i].strip().startswith('```'):
                    code_lines.append(lines[i])
                    i += 1
                blocks.append(self._create_code_block('\n'.join(code_lines), lang))
                i += 1
                continue
            
            # 图片（占位符）
            img_match = re.match(r'!\[([^\]]*)\]\(([^\)]+)\)', line)
            if img_match:
                alt_text = img_match.group(1)
                blocks.append({
                    "block_type": 2,
                    "text": {
                        "elements": [{"text_run": {"content": f"[图片: {alt_text}]"}}],
                        "style": {}
                    }
                })
                i += 1
                continue
            
            # 普通段落
            paragraph_lines = [line]
            while i + 1 < len(lines) and lines[i + 1].strip() and not re.match(r'^(#{1,6}\s+|[*\-+]|\d+\.|---)', lines[i + 1].strip()):
                paragraph_lines.append(lines[i + 1])
                i += 1
            
            paragraph_text = ' '.join([l.strip() for l in paragraph_lines if l.strip()])
            if paragraph_text:
                blocks.append(self._create_paragraph_block(paragraph_text))
            
            i += 1
        
        return blocks
    
    def _create_heading_block(self, level: int, text: str) -> Dict:
        """创建标题块"""
        level = min(max(level, 1), 9)
        heading_types = {
            1: "heading1", 2: "heading2", 3: "heading3",
            4: "heading4", 5: "heading5", 6: "heading6",
            7: "heading7", 8: "heading8", 9: "heading9"
        }
        heading_type = heading_types.get(level, "heading1")
        elements = self._parse_rich_text(text)
        
        return {
            "block_type": level + 2,
            heading_type: {
                "elements": elements,
                "style": {}
            }
        }
    
    def _create_paragraph_block(self, text: str) -> Dict:
        """创建段落块"""
        elements = self._parse_rich_text(text)
        return {
            "block_type": 2,
            "text": {
                "elements": elements,
                "style": {"align": 1}
            }
        }
    
    def _create_bullet_block(self, text: str) -> Dict:
        """创建无序列表块"""
        elements = self._parse_rich_text(text)
        return {
            "block_type": 12,
            "bullet": {
                "elements": elements,
                "style": {}
            }
        }
    
    def _create_ordered_block(self, text: str) -> Dict:
        """创建有序列表块"""
        elements = self._parse_rich_text(text)
        return {
            "block_type": 13,
            "ordered": {
                "elements": elements,
                "style": {}
            }
        }
    
    def _create_code_block(self, code: str, language: str = "") -> Dict:
        """创建代码块"""
        language_map = {
            "python": 40, "js": 23, "javascript": 23, "typescript": 49,
            "go": 20, "rust": 44, "java": 22, "c": 12, "cpp": 13,
            "shell": 46, "bash": 46, "sql": 47, "html": 21, "css": 17,
            "json": 3, "yaml": 2, "xml": 1, "markdown": 6
        }
        lang_enum = language_map.get(language.lower(), 1)
        
        return {
            "block_type": 14,
            "code": {
                "elements": [{"text_run": {"content": code}}],
                "style": {"language": lang_enum, "wrap": True}
            }
        }
    
    def _parse_rich_text(self, text: str) -> List[Dict]:
        """解析富文本"""
        if not text:
            return [{"text_run": {"content": ""}}]
        
        elements = []
        current_pos = 0
        
        patterns = [
            (r'\*\*\*(.+?)\*\*\*', 'bold', 'italic'),
            (r'\*\*(.+?)\*\*', 'bold', None),
            (r'\*(.+?)\*', None, 'italic'),
            (r'~~(.+?)~~', 'strikethrough', None),
            (r'`([^`]+)`', 'inline_code', None),
            (r'\[([^\]]+)\]\(([^\)]+)\)', 'link', None),
        ]
        
        matches = []
        for pattern, style1, style2 in patterns:
            for match in re.finditer(pattern, text):
                matches.append((match.start(), match.end(), match.group(0), match.groups(), style1, style2))
        
        matches.sort(key=lambda x: x[0])
        
        for match in matches:
            start, end, full_match, groups, style1, style2 = match
            
            if start > current_pos:
                plain_text = text[current_pos:start]
                if plain_text:
                    elements.append({"text_run": {"content": plain_text}})
            
            text_content = groups[0] if groups else ""
            text_style = {}
            if style1:
                text_style[style1] = True
            if style2:
                text_style[style2] = True
            
            if style1 == 'link':
                text_content = groups[0] if len(groups) > 0 else ""
                link_url = groups[1] if len(groups) > 1 else ""
                elements.append({
                    "text_run": {
                        "content": text_content,
                        "text_element_style": {"link": {"url": link_url}}
                    }
                })
            else:
                elements.append({"text_run": {"content": text_content, "text_element_style": text_style}})
            
            current_pos = end
        
        if current_pos < len(text):
            remaining = text[current_pos:]
            if remaining:
                elements.append({"text_run": {"content": remaining}})
        
        if not elements:
            elements = [{"text_run": {"content": text}}]
        
        return elements
    
    def write_content(self, obj_token: str, content: str) -> bool:
        """写入内容"""
        self._ensure_token()
        time.sleep(2)
        
        # 获取文档 block_id
        get_url = f"{self.base_url}/open-apis/docx/v1/documents/{obj_token}/blocks"
        get_req = urllib.request.Request(get_url, headers={'Authorization': f'Bearer {self.access_token}'})
        
        with urllib.request.urlopen(get_req, timeout=10) as response:
            get_resp = json.loads(response.read())
            parent_block_id = get_resp['data']['items'][0]['block_id']
        
        # 解析 Markdown
        blocks = self._parse_markdown_to_blocks(content)
        print(f"解析出 {len(blocks)} 个 blocks...")
        
        # 批量写入
        batch_size = 10
        for i in range(0, len(blocks), batch_size):
            batch = blocks[i:i+batch_size]
            
            add_url = f"{self.base_url}/open-apis/docx/v1/documents/{obj_token}/blocks/{parent_block_id}/children"
            add_data = json.dumps({"children": batch}).encode('utf-8')
            add_req = urllib.request.Request(
                add_url, data=add_data,
                headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {self.access_token}'}
            )
            
            try:
                with urllib.request.urlopen(add_req, timeout=30) as response:
                    add_resp = json.loads(response.read())
                    if add_resp.get('code') == 0:
                        print(f"  块 {i+1}-{min(i+batch_size, len(blocks))}: ✅")
                    else:
                        print(f"  块 {i+1}-{min(i+batch_size, len(blocks))}: ❌ {add_resp.get('msg')}")
            except Exception as e:
                print(f"  块 {i+1}-{min(i+batch_size, len(blocks))}: ❌ 异常")
            
            time.sleep(0.3)
        
        return True
    
    def create_and_write(self, title: str, content: str, parent_node_token: str = None) -> Dict:
        """创建文档并写入内容"""
        print(f"创建文档: {title}")
        doc = self.create_document(title, parent_node_token)
        print(f"✅ 文档创建成功: {doc['url']}")
        
        print(f"\n写入内容...")
        self.write_content(doc['obj_token'], content)
        
        return doc
    
    def validate_config(self) -> Dict:
        """验证配置"""
        result = {
            'app_id': '✅' if self.app_id else '❌',
            'app_secret': '✅' if self.app_secret else '❌',
            'space_id': '✅' if self.space_id else '❌',
            'token': '❌',
            'space_access': '❌'
        }
        
        try:
            self._get_token()
            result['token'] = '✅'
        except Exception as e:
            result['token'] = f'❌ {str(e)}'
            return result
        
        try:
            # 测试知识库访问
            url = f"{self.base_url}/open-apis/wiki/v2/spaces/{self.space_id}"
            req = urllib.request.Request(url, headers={'Authorization': f'Bearer {self.access_token}'})
            with urllib.request.urlopen(req, timeout=10) as response:
                resp = json.loads(response.read())
                if resp.get('code') == 0:
                    result['space_access'] = '✅'
                else:
                    result['space_access'] = f"❌ {resp.get('msg')}"
        except Exception as e:
            result['space_access'] = f'❌ {str(e)}'
        
        return result


def main():
    parser = argparse.ArgumentParser(description='飞书知识库文档写入器 - 增强版')
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # 全局参数
    parser.add_argument('--app-id', help='飞书应用 ID')
    parser.add_argument('--app-secret', help='飞书应用密钥')
    parser.add_argument('--space-id', help='知识库 Space ID')
    parser.add_argument('--wiki-domain', help='飞书域名')
    
    # create 命令
    create_parser = subparsers.add_parser('create', help='创建文档')
    create_parser.add_argument('title', help='文档标题')
    create_parser.add_argument('content', help='文档内容')
    create_parser.add_argument('--parent', '-p', help='父节点 token')
    
    # write_file 命令
    write_parser = subparsers.add_parser('write_file', help='从文件写入')
    write_parser.add_argument('title', help='文档标题')
    write_parser.add_argument('file', help='文件路径')
    write_parser.add_argument('--parent', '-p', help='父节点 token')
    
    # validate 命令
    validate_parser = subparsers.add_parser('validate', help='验证配置')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'validate':
            writer = LarkWikiWriter(
                app_id=args.app_id,
                app_secret=args.app_secret,
                space_id=args.space_id,
                wiki_domain=args.wiki_domain
            )
            result = writer.validate_config()
            print("📊 配置验证结果\n")
            print(f"APP_ID: {result['app_id']}")
            print(f"APP_SECRET: {result['app_secret']}")
            print(f"Space ID: {result['space_id']}")
            print(f"Token 获取: {result['token']}")
            print(f"知识库访问: {result['space_access']}")
            return
        
        writer = LarkWikiWriter(
            app_id=args.app_id,
            app_secret=args.app_secret,
            space_id=args.space_id,
            wiki_domain=args.wiki_domain
        )
        
        if args.command == 'create':
            doc = writer.create_and_write(args.title, args.content, args.parent)
            print(f"\n✅ 完成！文档链接: {doc['url']}")
        
        elif args.command == 'write_file':
            with open(args.file, 'r', encoding='utf-8') as f:
                content = f.read()
            doc = writer.create_and_write(args.title, content, args.parent)
            print(f"\n✅ 完成！文档链接: {doc['url']}")
    
    except ValueError as e:
        print(f"❌ 配置错误: {e}", file=sys.stderr)
        print("\n💡 提示: 请通过参数或环境变量提供配置", file=sys.stderr)
        print("   --app-id YOUR_APP_ID", file=sys.stderr)
        print("   --app-secret YOUR_APP_SECRET", file=sys.stderr)
        print("   --space-id YOUR_SPACE_ID", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
