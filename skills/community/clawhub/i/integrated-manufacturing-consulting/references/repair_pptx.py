"""PPTX文件修复脚本 — 彻底解决 XML 兼容性问题"""
import zipfile, shutil, tempfile, os, re

def repair_pptx(input_path, output_path):
    """深度修复PPTX文件：清理p:style、空ln标签、主题阴影引用等"""
    temp_dir = tempfile.mkdtemp()
    try:
        with zipfile.ZipFile(input_path, 'r') as z:
            z.extractall(temp_dir)
        
        for root, dirs, files in os.walk(temp_dir):
            for fname in files:
                if not fname.endswith('.xml'):
                    continue
                fpath = os.path.join(root, fname)
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original = content
                
                # 1. 彻底移除 p:style 节点（含子节点）
                content = re.sub(r'<p:style[^>]*>.*?</p:style>', '', content, flags=re.DOTALL)
                
                # 2. 移除 a:themeShadow 引用
                content = re.sub(r'<a:themeShadow[^>]*/>', '', content)
                content = re.sub(r'<a:themeShadow[^>]*>.*?</a:themeShadow>', '', content)
                
                # 3. 清理空的 a:ln 节点（没有子元素）
                content = re.sub(r'<a:ln[^>]*/>', '', content)
                content = re.sub(r'<a:ln[^>]*>\s*</a:ln>', '', content)
                
                # 4. 确保 a:latin 和 a:ea 有 typeface 属性
                content = re.sub(
                    r'<(a:latin)([^>]*)>',
                    lambda m: f'<a:latin typeface="Arial"{m.group(2)}>' if 'typeface' not in m.group(0) else m.group(0),
                    content
                )
                content = re.sub(
                    r'<(a:ea)([^>]*)>',
                    lambda m: f'<a:ea typeface="Microsoft YaHei"{m.group(2)}>' if 'typeface' not in m.group(0) else m.group(0),
                    content
                )
                
                # 5. 修复可能的 a:ln 中空 a:solidFill
                content = re.sub(r'<a:ln[^>]*><a:solidFill/>.*?</a:ln>', '', content)
                
                # 6. 清理空标签
                content = re.sub(r'<a:noFill/>', '<a:noFill/>', content)
                
                if content != original:
                    with open(fpath, 'w', encoding='utf-8') as f:
                        f.write(content)
        
        # 重新打包
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as z:
            for root, dirs, files in os.walk(temp_dir):
                for fname in files:
                    fpath = os.path.join(root, fname)
                    arcname = os.path.relpath(fpath, temp_dir)
                    z.write(fpath, arcname)
        print(f"✅ 修复完成: {output_path}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    inp = "input.pptx"
    out = "input_repaired.pptx"
    repair_pptx(inp, out)
