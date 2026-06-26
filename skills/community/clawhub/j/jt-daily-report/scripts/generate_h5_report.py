import json
import os
from datetime import datetime

def load_news_data():
    '加载新闻数据'
    data_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'daily_report.json')
    sorted_ids_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'sorted_ids.json')
    
    if not os.path.exists(data_file):
        print('错误：找不到新闻数据文件，请先运行 get_daily_report.py 获取数据')
        return None

    with open(data_file, 'r', encoding='utf-8') as f:
        ori_data = json.load(f)
    
    if not os.path.exists(sorted_ids_file):
        print('错误：找不到排序后的 ID 文件，直接返回原始数据')
        return ori_data
    
    with open(sorted_ids_file, 'r', encoding='utf-8') as f:
        sorted_ids = json.load(f)['sorted_ids']

    news = {}
    for item in ori_data['data']['news']:
        news[item['id']] = item

    data = {}
    data['data'] = {}
    data['data']['new'] = []
    for id in sorted_ids:
        if id in news:
            data['data']['new'].append(news[id])
   
    return data

def generate_h5_page(data):
    '生成 H5 页面'
    if 'data' in data and 'new' in data['data']:
        news_list = data['data']['new']
    elif 'data' in data and 'news' in data['data']:
        news_list = data['data']['news']
    elif 'news' in data:
        news_list = data['news']
    else:
        print('错误：数据格式不正确')
        return False
    
    html_content = '<!DOCTYPE html>\n'
    html_content += '<html lang="zh-CN">\n'
    html_content += '<head>\n'
    html_content += '    <meta charset="UTF-8">\n'
    html_content += '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
    html_content += '    <title>每日日报 - ' + datetime.now().strftime('%Y年%m月%d日') + '</title>\n'
    html_content += '    <style>\n'
    html_content += '        * { margin: 0; padding: 0; box-sizing: border-box; }\n'
    html_content += '        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; color: #333; }\n'
    html_content += '        .container { max-width: 800px; margin: 0 auto; }\n'
    html_content += '        .header { text-align: center; color: white; margin-bottom: 30px; padding: 20px; background: rgba(255, 255, 255, 0.1); border-radius: 15px; backdrop-filter: blur(10px); }\n'
    html_content += '        .header h1 { font-size: 2.5em; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }\n'
    html_content += '        .header .date { font-size: 1.2em; opacity: 0.9; }\n'
    html_content += '        .news-card { background: white; border-radius: 15px; padding: 20px; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); transition: transform 0.3s ease, box-shadow 0.3s ease; }\n'
    html_content += '        .news-card:hover { transform: translateY(-5px); box-shadow: 0 15px 40px rgba(0,0,0,0.2); }\n'
    html_content += '        .news-title { font-size: 1.3em; font-weight: bold; margin-bottom: 10px; color: #2c3e50; line-height: 1.4; }\n'
    html_content += '        .news-image { width: 100%; height: 200px; object-fit: cover; border-radius: 10px; margin-bottom: 15px; }\n'
    html_content += '        .news-abstract { color: #666; line-height: 1.6; margin-bottom: 15px; }\n'
    html_content += '        .news-meta { display: flex; justify-content: space-between; align-items: center; color: #999; font-size: 0.9em; }\n'
    html_content += '        .news-source { background: #f0f0f0; padding: 5px 10px; border-radius: 5px; }\n'
    html_content += '        .news-link { color: #667eea; text-decoration: none; font-weight: bold; transition: color 0.3s ease; }\n'
    html_content += '        .news-link:hover { color: #764ba2; }\n'
    html_content += '        .footer { text-align: center; color: white; margin-top: 40px; padding: 20px; background: rgba(255, 255, 255, 0.1); border-radius: 15px; }\n'
    html_content += '        @media (max-width: 600px) { .header h1 { font-size: 1.8em; } .news-title { font-size: 1.1em; } .news-image { height: 150px; } }\n'
    html_content += '    </style>\n'
    html_content += '</head>\n'
    html_content += '<body>\n'
    html_content += '    <div class="container">\n'
    html_content += '        <div class="header">\n'
    html_content += '            <h1>📰 每日日报</h1>\n'
    html_content += '            <div class="date">' + datetime.now().strftime('%Y年%m月%d日') + '</div>\n'
    html_content += '        </div>\n'
    
    for news in news_list:
        html_content += '        <div class="news-card">\n'
        html_content += '            <div class="news-title">' + news['title'] + '</div>\n'
        if news.get('picture'):
            html_content += '            <img src="' + news['picture'] + '" alt="新闻图片" class="news-image">\n'
        html_content += '            <div class="news-abstract">' + news['abstract'] + '</div>\n'
        html_content += '            <div class="news-meta">\n'
        html_content += '                <span class="news-source">' + news['source'] + '</span>\n'
        html_content += '                <a href="' + news['url'] + '" target="_blank" class="news-link">阅读全文 →</a>\n'
        html_content += '            </div>\n'
        html_content += '        </div>\n'
    
    html_content += '        <div class="footer">\n'
    html_content += '            <p>🤖 由智能助手生成 | 数据来源：本地新闻推荐 API</p>\n'
    html_content += '        </div>\n'
    html_content += '    </div>\n'
    html_content += '</body>\n'
    html_content += '</html>'
    
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, 'daily_report.html')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print('H5 页面生成成功！')
    print('文件路径：' + output_file)
    print('请在浏览器中打开查看效果')
    
    return True

def main():
    '主函数'
    print('开始生成 H5 日报页面...')
    
    data = load_news_data()
    if data:
        generate_h5_page(data)

if __name__ == '__main__':
    main()
