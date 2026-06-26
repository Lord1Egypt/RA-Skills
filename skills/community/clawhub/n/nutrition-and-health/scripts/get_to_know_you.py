#!/usr/bin/env python3
"""
了解用户 - 建立个人档案
"""

def get_to_know_you():
    """
    引导用户提供基本信息
    """
    questions = [
        ("年龄", "你多大了？"),
        ("性别", "你的性别是？"),
        ("身高", "你的身高是？"),
        ("体重", "你的体重是？"),
        ("健康状况", "有没有什么健康问题？比如三高、胃病、过敏等"),
        ("饮食习惯", "你喜欢吃什么？有什么忌口吗？"),
        ("运动习惯", "你平时运动吗？频率如何？"),
        ("作息时间", "你通常几点睡几点起？"),
        ("健康目标", "你的健康目标是什么？减脂、增肌、还是养生调理？")
    ]
    
    return questions

if __name__ == "__main__":
    print("让我了解你一下，这样我才能给出更贴心的建议！")
    print("你可以随时跳过不想回答的问题。")
    print()
    
    for key, question in get_to_know_you():
        answer = input(f"{question} ")
        if answer:
            print(f"好的，{key}：{answer}")
    print()
    print("感谢！现在我更了解你了，有什么健康问题随时问我！")
