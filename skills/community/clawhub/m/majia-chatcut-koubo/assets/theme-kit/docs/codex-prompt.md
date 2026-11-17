# 可直接交给 Codex 的任务模板

## 套用现有主题

```text
先读取 AGENTS.md、tokens/themes.json、tokens/layouts.json 和 docs/layout-spec.md。
把当前 9:16 口播页改为 sea-salt-cyan 主题与 fresh-frame 布局。
颜色只能使用 tokens/themes.css 的变量；保留 1080×1920 画布和安全区；
把人物素材放进 .talk-card__speaker，并保留透明背景模式。
修改后运行 node scripts/check-contrast.mjs，并检查 index.html 无溢出。
```

## 生成新一期口播页面

```text
读取本项目设计规范，基于 components/portrait-talk-card.* 新建一期口播页。
主题使用 emerald-gold，默认布局 executive-split。
文案：
栏目标签：会员运营复盘
主标题：权益不是越多越好，
而是越准越好
引导语：真正影响转化的是
强调词：权益匹配
CTA：先分层，再发券
页脚：把资源给到最需要的人
不要改变原始 4 色板，不新增依赖，输出可直接打开的 HTML。
```

## 接入 React

```text
以 examples/PortraitTalkCard.tsx 为起点，把组件接入现有 React 页面。
保留 data-theme / data-layout 接口；从 tokens/themes.ts 读取类型；
不要复制十六进制颜色；支持传入透明背景 video 作为 speaker。
```
