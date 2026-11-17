# 独立 HTML 诊断工具（远程获客用）

## 背景
本地生活老板大部分没有 Hermes/WorkBuddy，发 skill 给他们没法用。需要一个「双击就能用」的工具。

## 方案
把核心诊断逻辑（20题 + 评分 + 报告 + 联系方式）全部写在一个 HTML 文件里。
- 纯前端，零依赖
- 双击或用手机打开链接即可使用
- 数据只存在浏览器本地，不上传
- 末尾留微信/反馈页，方便成交

## 技术要点
- 单文件 HTML（所有 CSS/JS 内嵌）
- 移动端适配（老板用手机打开）
- GitHub Pages 或 CDN 托管
- 评分逻辑与 SKILL.md 中的 4 信号扣分制 + 5 维度评分一致

## 发布方式
- 推送到 GitHub gh-pages 分支：`https://<user>.github.io/<repo>/`
- 通过 jsdelivr CDN 加速国内访问：`https://cdn.jsdelivr.net/gh/<user>/<repo>@<branch>/<file>`

## 当前链接
- GitHub Pages：https://1027399464-tech.github.io/local-business-live-skills/
- CDN：https://cdn.jsdelivr.net/gh/1027399464-tech/local-business-live-skills@main/diagnosis-tool.html
