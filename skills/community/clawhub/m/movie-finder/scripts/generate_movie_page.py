#!/usr/bin/env python3
"""
Movie Page Generator
Generates an HTML page for movie playback with embedded player.
"""

import sys
import json
import argparse
from datetime import datetime
import os

# 电影类型映射
GENRE_MAP = {
    "科幻": "sci-fi",
    "动作": "action", 
    "喜剧": "comedy",
    "恐怖": "horror",
    "爱情": "romance",
    "动画": "animation",
    "悬疑": "mystery",
    "惊悚": "thriller",
    "冒险": "adventure",
    "奇幻": "fantasy",
    "剧情": "drama",
    "战争": "war",
    "纪录片": "documentary"
}

ENGLISH_GENRES = {v: k for k, v in GENRE_MAP.items()}

def generate_movie_html(title, year, rating, plot, poster_url, streaming_urls, other_sources=None):
    """生成电影播放页面 HTML"""
    
    other_sources_html = ""
    if other_sources:
        for src in other_sources:
            other_sources_html += f'<a href="{src["url"]}" target="_blank">{src["name"]}</a>'
    
    # 主播放源
    main_player = streaming_urls[0]["url"] if streaming_urls else ""
    
    html = f'''<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} ({year}) - 在线观看</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{ 
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); 
    color: #fff; 
    font-family: 'Segoe UI', Arial, sans-serif; 
    margin: 0; 
    padding: 20px; 
    min-height: 100vh;
  }}
  .container {{ max-width: 1000px; margin: 0 auto; }}
  .header {{ text-align: center; margin-bottom: 30px; }}
  .header h1 {{ 
    font-size: 2em; 
    margin: 0 0 10px; 
    background: linear-gradient(90deg, #e50914, #ff6b6b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }}
  .movie-info {{ 
    display: flex; 
    gap: 30px; 
    margin-bottom: 30px; 
    background: rgba(255,255,255,0.05);
    padding: 25px;
    border-radius: 15px;
    flex-wrap: wrap;
  }}
  .poster {{ flex: 0 0 220px; }}
  .poster img {{ 
    width: 100%; 
    border-radius: 10px; 
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
  }}
  .details {{ flex: 1; min-width: 280px; }}
  .details h2 {{ margin: 0 0 15px; font-size: 1.5em; }}
  .meta {{ display: flex; gap: 20px; margin-bottom: 15px; flex-wrap: wrap; }}
  .rating {{ 
    background: linear-gradient(90deg, #f5c518, #ffdb58);
    color: #000;
    padding: 5px 15px;
    border-radius: 20px;
    font-weight: bold;
  }}
  .year {{
    background: rgba(255,255,255,0.1);
    padding: 5px 15px;
    border-radius: 20px;
  }}
  .plot {{ 
    line-height: 1.8; 
    color: #ccc; 
    margin: 15px 0;
  }}
  .player-section {{ margin-top: 20px; }}
  .player-section h3 {{ margin-bottom: 15px; color: #e50914; }}
  .player-wrapper {{
    position: relative;
    padding-bottom: 56.25%; /* 16:9 */
    height: 0;
    overflow: hidden;
    border-radius: 10px;
    box-shadow: 0 10px 40px rgba(229,9,20,0.3);
  }}
  .player-wrapper iframe {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border: none;
  }}
  .sources {{ margin-top: 25px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.1); }}
  .sources h4 {{ margin: 0 0 10px; color: #888; }}
  .source-links {{ display: flex; gap: 10px; flex-wrap: wrap; }}
  .source-links a {{
    padding: 8px 16px;
    background: rgba(255,255,255,0.1);
    color: #4da6ff;
    text-decoration: none;
    border-radius: 5px;
    transition: all 0.3s;
  }}
  .source-links a:hover {{ background: rgba(77,166,255,0.2); }}
  .footer {{ text-align: center; margin-top: 40px; color: #666; font-size: 0.9em; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>🎬 电影放映厅</h1>
  </div>
  
  <div class="movie-info">
    <div class="poster">
      <img src="{poster_url}" alt="{title}" onerror="this.src='https://via.placeholder.com/220x330?text=No+Image'">
    </div>
    <div class="details">
      <h2>{title}</h2>
      <div class="meta">
        <span class="year">{year}</span>
        <span class="rating">★ {rating}/10</span>
      </div>
      <p class="plot">{plot}</p>
    </div>
  </div>
  
  <div class="player-section">
    <h3>▶ 直接播放</h3>
    <div class="player-wrapper">
      <iframe src="{main_player}" allowfullscreen></iframe>
    </div>
  </div>
  
  {f'''
  <div class="sources">
    <h4>备用播放源：</h4>
    <div class="source-links">
      {other_sources_html}
    </div>
  </div>
  ''' if other_sources else ''}
  
  <div class="footer">
    <p>🎬 {title} ({year}) · 由 Movie Finder Skill 生成 · {datetime.now().strftime('%Y-%m-%d')}</p>
  </div>
</div>
</body>
</html>'''
    
    return html


def main():
    parser = argparse.ArgumentParser(description='Generate movie playback HTML page')
    parser.add_argument('--title', required=True, help='电影标题')
    parser.add_argument('--year', required=True, help='上映年份')
    parser.add_argument('--rating', default='0', help='评分')
    parser.add_argument('--plot', default='', help='剧情简介')
    parser.add_argument('--poster', default='', help='海报URL')
    parser.add_argument('--player', required=True, help='主播放源URL')
    parser.add_argument('--sources', default='', help='备用源 JSON格式：[{{"name":"源1","url":"url1"}}]')
    parser.add_argument('--output', default='', help='输出文件路径')
    
    args = parser.parse_args()
    
    other_sources = []
    if args.sources:
        try:
            other_sources = json.loads(args.sources)
        except:
            pass
    
    html = generate_movie_html(
        title=args.title,
        year=args.year,
        rating=args.rating,
        plot=args.plot,
        poster_url=args.poster,
        streaming_urls=[{"url": args.player}],
        other_sources=other_sources if other_sources else None
    )
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"HTML page saved to: {args.output}")
    else:
        print(html)


if __name__ == '__main__':
    main()
