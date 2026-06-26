/**
 * Tavily 搜索提供者
 * AI 优化搜索，适合研究类查询
 */

export async function tavilySearch(query: string, maxResults: number = 10): Promise<any[]> {
  // 从环境变量获取 API Key
  const apiKey = process.env.TAVILY_API_KEY || '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';
  
  try {
    // 使用 Tavily API
    const response = await fetch('https://api.tavily.com/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
      },
      body: JSON.stringify({
        query: query,
        max_results: maxResults,
        search_depth: 'advanced',
        include_answer: true,
        include_images: false,
        include_raw_content: false
      })
    });
    
    if (!response.ok) {
      throw new Error(`Tavily API returned ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    
    return (data.results || []).map((result: any) => ({
      title: result.title,
      url: result.url,
      content: result.content,
      score: result.score,
      engine: 'tavily',
      published_date: result.published_date || null
    }));
  } catch (error) {
    console.error('[Search] Tavily search failed:', error.message);
    throw error;
  }
}
