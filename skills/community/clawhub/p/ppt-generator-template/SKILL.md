# PPT Generator Skill Template

## Description
一个简单的PPT生成器技能模板，用于演示如何创建OpenClaw技能。

## 功能说明
- 接收用户输入的演讲内容
- 自动分割成多个幻灯片
- 生成乔布斯风格的HTML演示文稿

## 使用示例
当用户说："帮我创建一个关于人工智能的PPT"时，这个技能会自动触发。

## 技能文件结构
```
ppt-generator-template/
├── SKILL.md          # 技能说明文件
├── index.js          # 主要逻辑文件
├── template.html     # HTML模板文件
└── assets/           # 资源文件目录
```

## 工作原理
1. 用户提供演讲内容
2. 技能将内容分割成逻辑段落（每个段落一个幻灯片）
3. 使用模板生成HTML文件
4. 输出可以直接在浏览器中打开的HTML文件

## 扩展功能建议
- 支持Markdown格式输入
- 添加CSS样式定制
- 支持图片插入
- 添加转场动画
- 导出为PDF格式