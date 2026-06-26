/**
 * 百度搜索模块
 */

export async function baiduSearch(apiKey, query, count = 10) {
  const url = "https://qianfan.baidubce.com/v2/ai_search/web_search";
  
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${apiKey}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        messages: [{ role: "user", content: query }],
        search_source: "baidu_search_v2",
        resource_type_filter: [{ type: "web", top_k: count }],
        search_recency_filter: "week"
      })
    });
    
    if (!response.ok) {
      throw new Error(`API错误: ${response.status}`);
    }
    
    const data = await response.json();
    
    const results = [];
    if (data.references) {
      for (const item of data.references) {
        results.push({
          title: item.title || "",
          url: item.url || "",
          snippet: item.content || item.snippet || "",
          date: item.date || ""
        });
      }
    }
    
    return results;
  } catch (e) {
    console.error(`搜索失败: ${e.message}`);
    return [];
  }
}
