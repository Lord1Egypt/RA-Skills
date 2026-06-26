---
name: lcsc
description: 通过 camoufox-cli 浏览器自动化操作立创商城，完成元器件搜索、查看详情、加入购物车、BOM 配单、PCB/SMT 下单等操作。Use when 用户需要搜索立创商城元器件、查看商品详情、加入购物车、BOM 配单、PCB/SMT 下单、查看订单等立创商城操作。
version: 1.0.0
metadata:
  openclaw:
    emoji: "🔌"
---

# 立创商城浏览器自动化助手

## 适用场景

当用户的任务涉及以下立创商城相关操作时，**必须通过 camoufox-cli 操作立创商城页面**：

- 搜索元器件（按型号、关键词、品牌）
- 查看商品详情（参数、价格、库存、封装、数据手册）
- 加入购物车
- 查看/管理购物车
- BOM 配单
- PCB/SMT 下单
- 查看订单状态、物流信息
- 查看优惠券、PLUS 会员权益
- 任何涉及立创商城的页面操作

## 如何调用

**camoufox-cli 路径**: `/opt/homebrew/bin/camoufox-cli`

必须使用上面的完整路径调用 camoufox-cli（它可能不在默认 PATH 中）。

```bash
# 打开立创商城首页
/opt/homebrew/bin/camoufox-cli open "https://www.szlcsc.com/"

# 获取当前页面 URL 和标题
/opt/homebrew/bin/camoufox-cli url
/opt/homebrew/bin/camoufox-cli title

# 获取页面交互元素（aria 树）
/opt/homebrew/bin/camoufox-cli snapshot -i

# 点击元素（使用 ref）
/opt/homebrew/bin/camoufox-cli click @e123

# 填写输入框（先清空再输入）
/opt/homebrew/bin/camoufox-cli fill @e456 "NE555"

# 输入文本（不清空）
/opt/homebrew/bin/camoufox-cli type @e456 "NE555"

# 按下按键（如 Enter）
/opt/homebrew/bin/camoufox-cli press Enter

# 滚动页面
/opt/homebrew/bin/camoufox-cli scroll down 500

# 等待元素加载或 URL 变化
/opt/homebrew/bin/camoufox-cli wait @e123
/opt/homebrew/bin/camoufox-cli wait --url https://www.szlcsc.com/search?q=NE555

# 获取元素文本
/opt/homebrew/bin/camoufox-cli text @e123

# 执行 JavaScript
/opt/homebrew/bin/camoufox-cli eval "document.title"
```

## 常用工作流程

### 1. 搜索元器件
```bash
# 打开立创商城首页
/opt/homebrew/bin/camoufox-cli open "https://www.szlcsc.com/"

# 等待搜索框加载
/opt/homebrew/bin/camoufox-cli wait @e123

# 填写搜索框并按回车搜索
/opt/homebrew/bin/camoufox-cli fill @e123 "NE555"
/opt/homebrew/bin/camoufox-cli press Enter

# 等待搜索结果加载
/opt/homebrew/bin/camoufox-cli wait --url https://www.szlcsc.com/search?q=NE555

# 获取搜索结果页面元素
/opt/homebrew/bin/camoufox-cli snapshot -i
```

### 2. 查看商品详情
```bash
# 点击商品链接
/opt/homebrew/bin/camoufox-cli click @e456

# 等待详情页加载
/opt/homebrew/bin/camoufox-cli wait --url https://item.szlcsc.com/

# 获取详情页文本或元素
/opt/homebrew/bin/camoufox-cli text @e789
/opt/homebrew/bin/camoufox-cli snapshot -i
```

### 3. 加入购物车
```bash
# 在商品详情页选择数量、规格
/opt/homebrew/bin/camoufox-cli fill @e123 "10"

# 点击“加入购物车”按钮
/opt/homebrew/bin/camoufox-cli click @e456

# 等待操作完成
/opt/homebrew/bin/camoufox-cli wait 2000
```

### 4. BOM 配单
```bash
# 打开 BOM 配单页面
/opt/homebrew/bin/camoufox-cli open "https://bom.szlcsc.com/bom.html"

# 等待页面加载
/opt/homebrew/bin/camoufox-cli wait @e123

# 上传 BOM 表或填写型号
# ...（根据页面元素操作）
```

### 5. PCB/SMT 下单
```bash
# 打开 PCB 下单页面
/opt/homebrew/bin/camoufox-cli open "https://www.jlc.com/newOrder/#/pcb/pcbPlaceOrder"

# 等待页面加载
/opt/homebrew/bin/camoufox-cli wait @e123

# 填写参数、上传文件
# ...（根据页面元素操作）
```

## camoufox-cli 常用命令速查

| 命令 | 用途 | 关键参数 |
|------|------|----------|
| open <url> | 导航到 URL | url |
| back | 返回上一页 | - |
| forward | 前进到下一页 | - |
| reload | 刷新页面 | - |
| url | 打印当前 URL | - |
| title | 打印页面标题 | - |
| snapshot [-i] [-s sel] | 获取页面元素树 | -i: 交互模式, -s: 限定范围 |
| click @ref | 点击元素 | ref |
| fill @ref "text" | 清空输入框并输入文本 | ref, text |
| type @ref "text" | 不清空直接输入文本 | ref, text |
| select @ref "option" | 选择下拉选项 | ref, option |
| check @ref | 切换复选框 | ref |
| hover @ref | 悬停在元素上 | ref |
| press <key> | 按下按键 | key (如 Enter, Control+a) |
| text @ref\|selector | 获取元素文本内容 | ref 或 selector |
| eval "js expression" | 执行 JavaScript | js 表达式 |
| screenshot [--full] [f] | 截图到文件或 stdout | --full: 全屏, f: 文件路径 |
| pdf <file> | 保存页面为 PDF | 文件路径 |
| scroll <dir> [px] | 滚动页面 | dir: up/down, px: 像素数（默认 500） |
| wait <ms\|@ref\|--url p> | 等待时间/元素/URL | ms: 毫秒数, @ref: 元素, --url: URL |
| tabs | 列出打开的标签页 | - |
| switch <index> | 切换标签页 | 标签页索引 |
| close-tab | 关闭当前标签页 | - |
| sessions | 列出活动会话 | - |
| cookies [import\|export] | 管理 cookies | import/export |

## 注意事项

- 点击或导航后需等待页面加载（使用 wait 命令），再读取新内容
- 使用 snapshot -i 获取交互元素树，找到合适的 ref 再操作
- fill 命令会先清空输入框再输入，适合搜索框等场景
- type 命令不会清空输入框，适合追加内容
- 优先使用 camoufox-cli 的专用命令（snapshot, click, fill 等），eval 作为补充
