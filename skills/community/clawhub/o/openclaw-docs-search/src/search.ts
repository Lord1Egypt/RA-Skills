import { JSDOM } from 'jsdom';
import TurndownService from 'turndown';

export interface RawSearchResult {
  page: string;
  header: string;
  content: string;
  metadata?: {
    title?: string;
    breadcrumbs?: string[];
    [key: string]: any;
  };
  score?: number;
}

export interface RawSearchResponse {
  results: RawSearchResult[];
}

function formatResultsToMarkdown(data: RawSearchResponse): string {
  if (!data || !data.results || data.results.length === 0) {
    return "未找到相关文档结果。";
  }

  const markdownParts = data.results.map((result, index) => {
    // 提取有用的元数据，丢弃无用的 icon、hash、score 等
    const title = result.metadata?.title || result.header || '未知标题';
    const breadcrumbs = result.metadata?.breadcrumbs?.join(' > ') || title;
    
    // 清理 content，去除多余的空行和重复的头部标题
    let cleanContent = result.content ? result.content.trim() : '无内容';
    // 去除 HTML 标签，例如搜索高亮的 <mark> 和 <b> 标签
    cleanContent = cleanContent.replace(/<\/?[^>]+(>|$)/g, "");
    
    if (title && cleanContent.startsWith(title)) {
      cleanContent = cleanContent.substring(title.length).trim();
    }
    // 确保换行不会导致 Markdown 格式被破坏，将多余的换行替换为空格
    cleanContent = cleanContent.replace(/\n+/g, ' ');
    
    // 构建 Markdown 块
    return `### ${index + 1}. ${breadcrumbs}\n- **路径**: \`${result.page}\`\n- **内容**: ${cleanContent}`;
  });

  return markdownParts.join('\n\n');
}

export async function searchOpenclaw(query: string, language: 'zh-Hans' | 'en' = 'en'): Promise<string> {
  const url = 'https://leaves.mintlify.com/api/search/clawdhub';
  const headers = {
    'Content-Type': 'application/json',
  };
  const body = JSON.stringify({
    query: query,
    filters: {
      language: language,
    },
  });

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: headers,
      body: body,
    });

    if (!response.ok) {
      throw new Error(`HTTP Error: ${response.status} ${response.statusText}`);
    }

    const data: RawSearchResponse = await response.json();
    
    // 将原始 JSON 转换为精简的 Markdown 格式
    return formatResultsToMarkdown(data);
  } catch (error) {
    console.error('Failed to search openclaw:', error);
    throw error;
  }
}

/**
 * 获取指定页面路径的文档详情并转换为 Markdown
 * @param pagePath 文档页面路径，例如 "zh-CN/concepts/queue"
 * @returns 转换后的 Markdown 字符串
 */
export async function getOpenclawDoc(pagePath: string): Promise<string> {
  // 拼接完整 URL
  const baseUrl = 'https://docs.openclaw.ai/';
  // 移除路径开头可能存在的斜杠，防止拼接出双斜杠
  const cleanPath = pagePath.startsWith('/') ? pagePath.slice(1) : pagePath;
  const fullUrl = `${baseUrl}${cleanPath}`;

  try {
    // 1. 获取 HTML 页面
    const response = await fetch(fullUrl);
    if (!response.ok) {
      throw new Error(`Failed to fetch document: HTTP ${response.status} ${response.statusText}`);
    }
    const htmlText = await response.text();

    // 2. 解析 HTML 并提取 #content-area 元素
    const dom = new JSDOM(htmlText);
    const document = dom.window.document;
    const contentArea = document.getElementById('content-area');

    if (!contentArea) {
      return `错误: 未在页面 (${fullUrl}) 中找到 id="content-area" 的元素。`;
    }

    // 3. 将提取的 HTML 转换为 Markdown
    const turndownService = new TurndownService({
      headingStyle: 'atx',
      codeBlockStyle: 'fenced'
    });
    
    // 可以添加针对特定 HTML 结构的自定义转换规则，如果有需要的话
    // turndownService.addRule(...)

    const markdown = turndownService.turndown(contentArea.innerHTML);
    
    // 添加来源标识，方便 LLM 了解数据来源
    return `> 来源: ${fullUrl}\n\n${markdown}`;

  } catch (error) {
    console.error(`Failed to get document for path: ${pagePath}`, error);
    throw error;
  }
}

// 简单测试入口
if (require.main === module) {
  const mode = process.argv[2] || 'search';
  
  if (mode === 'search') {
    const query = process.argv[3] || 'timeout';
    const language = (process.argv[4] as 'zh-Hans' | 'en') || 'en';
    
    searchOpenclaw(query, language).then(markdown => {
      console.log('\n--- 格式化后的 Markdown 搜索结果 ---\n');
      console.log(markdown);
      console.log('\n------------------------------------\n');
    }).catch(err => {
      console.error(err);
    });
  } else if (mode === 'doc') {
    const docPath = process.argv[3] || 'zh-CN/concepts/queue';
    
    getOpenclawDoc(docPath).then(markdown => {
      console.log(`\n--- 文档 [${docPath}] 内容 ---\n`);
      console.log(markdown);
      console.log('\n------------------------------------\n');
    }).catch(err => {
      console.error(err);
    });
  } else {
    console.log('未知模式。请使用 "search <关键字>" 或 "doc <页面路径>"');
  }
}
