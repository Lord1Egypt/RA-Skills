# 图示使用说明

本 Skill 的策略图采用 Diagram Design 的 editorial SVG 规范：浅灰纸张、深墨文字、蓝灰关系线、单一橙色焦点；图形使用正交连线、明确箭头、有限节点和可读字号，避免阴影、霓虹、渐变和每项都上色。

真实软件操作图与策略图分开使用：`assets/wps/` 下的三张“annotated.svg”是把本机 WPS 实测截图与标注合并后的自包含主图（无需外部图片文件），应作为字数统计教程的主图；同目录 PNG 是可选的原始截图源。下面两张 SVG 只用于解释产品选择与计费逻辑，不要把策略图当成 WPS 操作截图。

- `assets/wps/01-paper-open-annotated.png`：打开完整论文稿件；
- `assets/wps/02-review-tab-annotated.png`：进入审阅并核对状态栏；
- `assets/wps/03-word-count-annotated.png`：实机统计窗口与字段解读。

- `assets/product-selection-strategy.svg`：通用产品选择图，用于“我该选哪个版本”答疑；图中文字不绑定具体品牌或站点。
- `assets/character-billing-flow.svg`：通用字符统计与计费流程图。图中强调“平台解析优先于本地预估”，并将按篇与按字符分到不同结算路径。

引用 SVG 时保留 `role="img"`、`<title>`、`<desc>` 和图外文字说明；在窄屏页面使用响应式容器，不把图中文字缩放到无法阅读。动态价格和产品名放在图外的实时表格里，避免资产过期。
