import requests
import json
import os
import sys

def save_news_data(data):
    '保存新闻数据到JSON文件'
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    data_file = os.path.join(data_dir, 'daily_report.json')
    
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return data_file

def get_general_news():
    api_url = 'https://jiutian.10086.cn/jiujiuassist/proactive/get_user_news_recommend'
    # api_url = 'http://localhost:10819/proactive/get_user_news_recommend'

    try:
        print('正在获取每日日报数据...')
        
        # 发送 POST 请求
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print('数据获取成功！')
            
            # 保存数据
            data_file = save_news_data(data)
            print('数据已保存到：' + data_file)
            
            # # 显示简要信息
            # if 'data' in data and 'news' in data['data']:
            #     news_count = len(data['data']['news'])
            #     print('共获取 ' + str(news_count) + ' 条新闻')
                
            #     # 显示前3条新闻标题
            #     print('\n热门新闻预览：')
            #     for i, news in enumerate(data['data']['news'][:3], 1):
            #         print(str(i) + '. ' + news['title'])
            
            # # 自动生成H5页面
            # print('\n正在生成H5页面...')
            # sys.path.insert(0, os.path.dirname(__file__))
            # import generate_h5_report
            # generate_h5_report.main()
            
        else:
            print('请求失败，状态码：' + str(response.status_code))
            print('响应内容：' + response.text)
            
    except requests.exceptions.Timeout:
        print('请求超时，请检查本地服务是否正常运行')
    except requests.exceptions.ConnectionError:
        print('连接失败，请检查本地服务是否已启动')
    except Exception as e:
        print('发生异常：' + str(e))

    

if __name__ == '__main__':
    # userid = sys.argv[1]
    get_general_news()
