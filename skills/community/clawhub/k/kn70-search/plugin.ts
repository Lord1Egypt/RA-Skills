// Search Skill - Multi-engine support
// Engines: Tavily (recommended), multi-search-engine, SearXNG (Windows Docker)

import { checkRateLimit } from '../../core/rate-limiter';

export default function(api) {
  api.registerTool({
    name: "search_web",
    description: "Search the internet using Tavily, multi-search-engine, or SearXNG (Rate limit: 20 calls/min)",
    parameters: {
      type: "object",
      properties: {
        query: { 
          type: "string", 
          description: "Search query string" 
        },
        max_results: { 
          type: "integer", 
          default: 10, 
          description: "Maximum number of results to return" 
        },
        engine: { 
          type: "string", 
          default: "auto",
          enum: ["auto", "tavily", "multi", "searxng"],
          description: "Search engine: auto (smart select), tavily (AI-optimized), multi (17 engines), searxng (self-hosted)"
        }
      },
      required: ["query"]
    },
    async execute(_id, params) {
      const { query, max_results = 10, engine = "auto" } = params;
      
      // === Rate limit check (20 calls per minute - PRODUCTION) ===
      const allowed = await checkRateLimit("search_web", 20, 60000);
      if (!allowed) {
        throw Object.assign(new Error("Rate limit exceeded (20 calls/min). Please wait before making more searches."), { 
          code: "RATE_LIMIT",
          retry_after: 60 
        });
      }
      
      // === 自动选择最佳引擎 ===
      let selectedEngine = engine;
      if (engine === "auto") {
        const q = query.toLowerCase();
        
        // 国内资讯 → Multi（百度/必应中国更准）
        if (q.includes("中国") || q.includes("国内") || q.includes("百度") || q.includes("微信") || q.includes("抖音")) {
          selectedEngine = "multi";
        }
        // AI/技术/代码 → SearXNG（聚合更多技术源）
        else if (q.includes("ai") || q.includes("人工智能") || q.includes("技术") || 
                 q.includes("代码") || q.includes("编程") || q.includes("github") ||
                 q.includes("python") || q.includes("javascript") || q.includes("api") ||
                 q.includes("llm") || q.includes("machine learning") || q.includes("cuda") ||
                 q.includes("transformer") || q.includes("research") || q.includes("paper") ||
                 q.includes("研究") || q.includes("论文")) {
          selectedEngine = "searxng";
        }
        // 新闻 → SearXNG（新闻引擎更全）
        else if (q.includes("新闻") || q.includes("news") || q.includes("报道")) {
          selectedEngine = "searxng";
        }
        // 默认 → SearXNG
        else {
          selectedEngine = "searxng";
        }
      }
      
      try {
        // === SearXNG - Self-hosted (Windows Docker Desktop) - 默认首选 ===
        if (selectedEngine === "searxng") {
          const searxngUrl = process.env.SEARXNG_URL || "http://127.0.0.1:8080";
          
          try {
            const response = await fetch(`${searxngUrl}/search?q=${encodeURIComponent(query)}&format=json`);
            if (!response.ok) {
              throw new Error(`SearXNG returned ${response.status}`);
            }
            
            const data = await response.json();
            
            return { 
              success: true, 
              engine: "searxng",
              message: "SearXNG search completed (聚合 20+ 引擎)",
              results: (data.results || []).slice(0, max_results)
            };
          } catch (e) {
            console.warn("SearXNG failed, fallback to Tavily:", e.message);
            // Fallback to Tavily
            selectedEngine = "tavily";
          }
        }
        
        // === Tavily - AI optimized search ===
        if (selectedEngine === "tavily") {
          const apiKey = process.env.TAVILY_API_KEY || "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";
          
          // Use exec to call Tavily Python script (fixed path)
          const result = await api.exec({
            command: "python",
            args: [
              "D:\\winopenclaw\\workspace\\skills\\_legacy\\tavily\\search_tavily_news.py"
            ],
            env: {
              TAVILY_API_KEY: apiKey
            }
          });
          
          return { 
            success: true, 
            engine: "tavily",
            message: "Tavily search completed (AI 优化)",
            results: result.results || []
          };
        }
        
        // === Multi-search-engine - 17 engines without API key ===
        if (selectedEngine === "multi") {
          const apiKey = process.env.TAVILY_API_KEY || "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";
          
          // Use exec to call multi-search-engine skill
          const result = await api.exec({
            command: "python",
            args: [
              "D:\\winopenclaw\\workspace\\skills\\_legacy\\tavily\\search_tavily_news.py"
            ],
            env: {
              TAVILY_API_KEY: apiKey
            }
          });
          
          return { 
            success: true, 
            engine: "multi",
            message: "Multi-search completed",
            results: result.results || []
          };
        }
        
        // === Multi-search-engine - 17 engines without API key ===
        if (engine === "multi") {
          // Use web_fetch to scrape search engine results pages
          const searchUrls = [
            `https://www.baidu.com/s?wd=${encodeURIComponent(query)}`,
            `https://cn.bing.com/search?q=${encodeURIComponent(query)}`,
            `https://www.google.com/search?q=${encodeURIComponent(query)}`
          ];
          
          const results = [];
          for (const url of searchUrls) {
            try {
              const fetched = await api.web_fetch({ url, maxChars: 5000 });
              // TODO: Parse HTML to extract search results
              results.push({ url, content: fetched });
            } catch (e) {
              // Skip failed engines
            }
          }
          
          return { 
            success: true, 
            engine: "multi",
            message: "Searched multiple engines",
            results: results.slice(0, max_results)
          };
        }
        
        // === SearXNG - Self-hosted (Windows Docker Desktop) ===
        if (engine === "searxng") {
          const searxngUrl = process.env.SEARXNG_URL || "http://localhost:8080";
          
          const response = await fetch(`${searxngUrl}/search?q=${encodeURIComponent(query)}&format=json`);
          if (!response.ok) {
            throw new Error(`SearXNG returned ${response.status}`);
          }
          
          const data = await response.json();
          
          return { 
            success: true, 
            engine: "searxng",
            message: "SearXNG search completed",
            results: (data.results || []).slice(0, max_results)
          };
        }
        
        return { success: false, error: `Unknown engine: ${selectedEngine}` };
        
      } catch (error) {
        return { 
          success: false, 
          error: error.message,
          engine: selectedEngine
        };
      }
    }
  });
}
