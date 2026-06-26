# OCAX Passport

🆔 节点身份证技能 - 为计算资源提供者生成硬件档案和信誉评分

## 功能

- 自动获取节点硬件信息 (CPU/GPU/内存/存储)
- 计算智能信誉评分
- 生成节点身份证 (Passport ID / Node ID)
- 检测支持的任务类型
- 支持自动更新

## 安装

```bash
# 克隆技能
git clone https://github.com/HKUDS/OCAX-Passport.git
cd OCAX-Passport

# 安装依赖
pip install -r requirements.txt
```

## 使用方法

```python
from ocax_passport import generate_passport

# 生成节点护照
passport = generate_passport("My-Node", "User-Name")

# 获取信息
print(passport.to_json())

# 获取评分
print(passport.scores)
```

## 命令行

```bash
# 获取节点护照
python tool.py passport

# 查看硬件信息
python tool.py hardware

# 查看评分
python tool.py scores
```

## 依赖

- psutil>=5.9.0

## 版本

v1.0.0

## 许可证

MIT
