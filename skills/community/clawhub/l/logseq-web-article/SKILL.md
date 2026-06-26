---
name: "logseq-web-article"
description: "Fetch article content from general web page URLs, and call logseq-article-archive to organize, summarize, and archive the content. Call this skill when users need to process web articles and organize them into Logseq."
---

# Web Article Processor

## Feature Description

This skill can:
1. Receive general web page URLs from users
2. Fully fetch the complete article content without any modification, preserve the original content, convert it to Markdown format, and process it according to the following rules:
   - Use Markdown heading format (#) for titles
   - Add "- " before each paragraph to form list format
   - Use blockquote format (>) for quoted content
   - Use indentation for nested lists
   - Use bold format (**) for important content
3. Record meta information such as the web address at the end of the article
4. Check if logseq-article-archive skill is installed; if not, install it automatically
5. Call the logseq-article-archive skill for secondary analysis, summarization, and archiving of the article content
6. Return the processed results to the user

## Usage

Call this skill directly when users provide web article URLs and wish to organize the content into Logseq.

### Input Format

Users only need to provide the complete URL of the web article, for example:
```
https://example.com/article/abc123
https://mp.weixin.qq.com/s/abc123def456
https://www.zhihu.com/article/123456
```

### Processing Flow

1. Receive the web article URL provided by the user
2. Use the WebFetch tool to fetch the complete article content
3. Save the original article content without any modification, convert it to Markdown format, and process it according to the following rules:
   - Use Markdown heading format (#) for titles
   - Add "- " before each paragraph to form list format
   - Use blockquote format (>) for quoted content
   - Use indentation for nested lists
   - Use bold format (**) for important content
4. Record meta information such as the web address at the end of the article
5. Check if logseq-article-archive skill is installed
6. If logseq-article-archive is not installed, install it automatically
7. Call the logseq-article-archive skill for secondary analysis, summarization, and archiving of the article content
8. Return the organized results to the user

## Notes

- Ensure the provided URL is a valid web article link
- Some web articles may require login to access, in which case the content may not be retrievable
- Some web pages may contain excessive ads or irrelevant content, it is recommended to select article links with clear content
- The processing may take some time, please be patient
- This skill requires logseq-article-archive skill for secondary processing. It will be installed automatically if not present.

## Examples

**User Input:**
```
Please process this article: https://example.com/article/abc123
```

**Skill Output:**
```
Article content has been fetched and organized via logseq-article-archive skill. Results are as follows:

# Article Title
- Author: XXX
- Publication Date: YYYY-MM-DD

## Core Content
- Key Point 1
- Key Point 2
- Key Point 3

## Summary
...

---

## Article Meta Information
- Original Link: https://example.com/article/abc123
- Fetch Time: YYYY-MM-DD HH:MM:SS
- Processing Tool: logseq-web-article
```

---

# 网页文章处理器（中文介绍）

## 功能说明

此技能可以：
1. 接收用户输入的通用网页URL
2. 完整获取文章的完整内容，不做任何修改，保留原文内容，转换成Markdown格式，并按照以下格式进行处理：
   - 标题使用Markdown的标题格式（#）
   - 每个段落前添加"- "符号，形成列表格式
   - 引用内容使用blockquote格式（>）
   - 嵌套列表使用缩进
   - 重点内容使用加粗格式（**）
3. 在文章结尾记录文章的网络地址等信息
4. 检查 logseq-article-archive 技能是否已安装；如果未安装，则自动安装
5. 调用 logseq-article-archive 技能对文章内容进行二次分析、总结和归档
6. 将处理结果返回给用户

## 使用方法

当用户提供网页文章地址并希望将其内容整理到Logseq中时，直接调用此技能。

### 输入格式

用户只需提供网页文章的完整URL，例如：
```
https://example.com/article/abc123
https://mp.weixin.qq.com/s/abc123def456
https://www.zhihu.com/article/123456
```

### 处理流程

1. 接收用户提供的网页文章URL
2. 使用WebFetch工具获取文章的完整内容
3. 保存原始文章内容，不做任何修改，格式转换成Markdown格式，并按照以下格式进行处理：
   - 标题使用Markdown的标题格式（#）
   - 每个段落前添加"- "符号，形成列表格式
   - 引用内容使用blockquote格式（>）
   - 嵌套列表使用缩进
   - 重点内容使用加粗格式（**）
4. 在文章结尾记录文章的网络地址等元信息
5. 检查 logseq-article-archive 技能是否已安装
6. 如果 logseq-article-archive 未安装，自动安装该技能
7. 调用 logseq-article-archive 技能对文章内容进行二次分析、总结和归档
8. 返回整理后的结果给用户

## 注意事项

- 确保提供的URL是有效的网页文章链接
- 部分网页文章可能需要登录才能访问，此时可能无法获取内容
- 部分网页可能包含较多广告或无关内容，建议选择内容清晰的文章链接
- 处理过程可能需要一定时间，请耐心等待
- 此技能需要 logseq-article-archive 技能进行二次处理，如果尚未安装，将自动安装

## 示例

**用户输入：**
```
请处理这篇文章：https://example.com/article/abc123
```

**技能输出：**
```
已获取文章内容并通过 logseq-article-archive 技能进行整理，结果如下：

# 文章标题
- 作者：XXX
- 发布时间：YYYY-MM-DD

## 核心内容
- 要点1
- 要点2
- 要点3

## 总结
...

---

## 文章元信息
- 原文链接：https://example.com/article/abc123
- 获取时间：YYYY-MM-DD HH:MM:SS
- 处理工具：logseq-web-article
```