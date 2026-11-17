# HTML 自助诊断工具制作流程

为 local-business-live-cycle skill 生成独立 HTML 诊断工具，用于远程获客。

## 适用场景
老板不需要装 Hermes/WorkBuddy，双击 HTML 文件或在浏览器打开链接即可使用。

## 制作步骤
1. 将 SKILL.md 中的 20 道诊断题（A-F 组）转为前端问卷
2. 嵌入评分逻辑：4信号扣分制 + 5维评分 + 到店承接判断
3. 报告输出：综合评分 + 等级 + 核心判断 + 3条行动建议
4. 末尾留反馈入口（微信或 Notion 链接）
5. 输出为单文件 HTML（纯前端，无需后端）

## 托管方案
- GitHub Pages（国际可用，Content-Type 正确）
- jsdelivr CDN（国内快，但 Content-Type 为 text/plain，部分浏览器可能显示源码）
- 独立部署到国内 CDN/对象存储

## 用户路径
老板收到链接 → 打开 → 逐题点选 → 自动出报告 → 报告末尾有反馈入口 → 加微信成交
