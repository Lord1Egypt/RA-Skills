## 快速开始

```bash
# 1️⃣ 进入文件夹
cd libtv-qunqin

# 2️⃣ 安装依赖（请确保你已激活 OpenClaw 的 venv）
pip install -r requirements.txt

# 3️⃣ 准备一份故事文本（示例：novel/寻秦记.txt）
echo "秦始皇的天下…" > novel/寻秦记.txt

# 4️⃣ 运行测试
cat <<EOF | python libtv_qunqin.py
{
  "story_file": "novel/寻秦记.txt",
  "panel_count": 4,
  "font": "Noto Serif SC",
  "output_dir": "./demo"
}
EOF

# 5️⃣ 检查输出
ls demo   # 会看到 PNG 图像和 result.json