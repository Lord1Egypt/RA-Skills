# -*- coding: utf-8 -*-

import requests


def get_answer(query):
    """
    获取医疗问题的答案。

    Args:
        query: 用户输入的医疗问题
    Returns:
        答案
    """
    url = "https://shangbao.yunzhisheng.cn/skills/medical-qa/unisound_zhiyi_service"
    headers = {'Content-Type': 'application/json'}
    input_data = {"query": query}
    for i in range(3):
        response = requests.post(url, headers=headers, json=input_data, timeout=600)
        if response.status_code == 200:
            response_json = response.json()
            status = response_json["status"]
            if status == 1:
                answer = response_json["answer"]
                return answer
    return None

if __name__ == "__main__":
    query = "感冒了要不要吃抗生素（消炎药）？" # 问题
    answer = get_answer(query)
    print(answer)

