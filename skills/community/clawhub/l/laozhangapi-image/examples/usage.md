# 使用示例

## 文生图

### 基础用法
```bash
# 生成图片（默认 sora_image，$0.01/张）
python scripts/generate_image.py "一只可爱的猫咪在花园里玩耍"

# 指定比例
python scripts/generate_image.py "夕阳海滩风景" --ratio 3:2
python scripts/generate_image.py "人物肖像" --ratio 2:3
python scripts/generate_image.py "APP图标" --ratio 1:1

# 保存到指定位置
python scripts/generate_image.py "可爱小狗" --output ~/Pictures/dog.png

# 使用其他模型
python scripts/generate_image.py "未来城市" --model gemini-3-pro-image-preview
```

### 实际场景
```bash
# 小红书封面（3:2横版）
python scripts/generate_image.py "一个穿着汉服的女孩在樱花树下，唯美，梦幻" --ratio 3:2

# 手机壁纸（2:3竖版）
python scripts/generate_image.py "极简风格的山景，渐变天空" --ratio 2:3

# 头像（1:1正方形）
python scripts/generate_image.py "可爱的卡通龙虾角色，大眼睛，微笑" --ratio 1:1
```

## 图片编辑

### 基础编辑
```bash
# 简单修改
python scripts/edit_image.py "https://example.com/cat.jpg" "把猫咪的毛色改成彩虹色"

# 美化照片
python scripts/edit_image.py "https://example.com/photo.jpg" "美化这张照片，让光线更柔和"

# 换背景
python scripts/edit_image.py "https://example.com/person.jpg" "把背景换成巴黎铁塔"
```

### 预设风格
```bash
# 卡通化
python scripts/edit_image.py "https://example.com/photo.jpg" --style 卡通

# 油画风格
python scripts/edit_image.py "https://example.com/landscape.jpg" --style 油画

# 水墨画
python scripts/edit_image.py "https://example.com/mountain.jpg" --style 水墨
```

### 多图融合
```bash
# 融合两张图
python scripts/edit_image.py "https://a.jpg,https://b.jpg" "将两张图片融合成一张"

# 合成场景
python scripts/edit_image.py "https://person.jpg,https://background.jpg" "把人物放到背景中"
```

## 高级用法

### 详细输出
```bash
# 查看详细信息
python scripts/generate_image.py "测试图片" --verbose

# 输出完整JSON响应
python scripts/generate_image.py "测试图片" --json
```

### 不保存图片
```bash
# 仅获取URL，不保存到本地
python scripts/generate_image.py "测试图片" --no-save
```

### 指定 Token
```bash
# 临时使用其他 token
python scripts/generate_image.py "测试图片" --token sk-xxx
```
