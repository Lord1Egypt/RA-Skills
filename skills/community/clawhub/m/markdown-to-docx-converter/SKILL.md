# md2word Skill

## Description
A skill that converts .md files to Word files. When users send .md files, it automatically accesses the `https://md2word.com/en` website, uploads the file, and downloads the converted Word file.

## Input Format
- Accepts .md files sent by users

## Output Format
- Returns the converted Word file to users

## Workflow
1. Receive .md file from user
2. Access `https://md2word.com/en` website
3. Upload .md file to the website
4. Wait for conversion to complete
5. Download the converted Word file
6. Return the Word file to the user

## Dependencies
- requests
- beautifulsoup4

---

## 功能描述
将.md文件转换为Word文件的技能。当用户发送.md文件时，自动访问 `https://md2word.com/en` 网站，上传文件并下载转换后的Word文件。

## 输入格式
- 接收用户发送的.md文件

## 输出格式
- 向用户返回转换后的Word文件

## 工作流程
1. 接收用户发送的.md文件
2. 访问 `https://md2word.com/en` 网站
3. 上传.md文件到网站
4. 等待转换完成
5. 下载转换后的Word文件
6. 将Word文件返回给用户

## 依赖
- requests
- beautifulsoup4