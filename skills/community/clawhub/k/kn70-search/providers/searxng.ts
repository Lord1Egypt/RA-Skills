/**
 * SearXNG 搜索提供者
 * 自托管元搜索引擎，聚合多个引擎结果
 */

export async function searxngSearch(query: string, maxResults: number = 10): Promise<any[]> {
  const searxngUrl = process.env.SEARXNG_URL || 'http://localhost:8080';
  
  try {
    const url = new URL('/search', searxngUrl);
    url.searchParams.set('q', query);
    url.searchParams.set('format', 'json');
    url.searchParams.set('limit', maxResults.toString());
    
    const response = await fetch(url.toString());
    if (!response.ok) {
      throw new Error(`SearXNG returned ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    
    if (!data.results || !Array.isArray(data.results)) {
      return [];
    }
    
    return data.results.slice(0, maxResults).map((result: any) => ({
      title: result.title,
      url: result.url,
      content: result.content || '',
      engine: 'searxng',
      published_date: result.publishedDate || null,
      img_src: result.img_src || null
    }));
  } catch (error) {
    console.error('[Search] SearXNG search failed:', error.message);
    throw error;
  }
}
