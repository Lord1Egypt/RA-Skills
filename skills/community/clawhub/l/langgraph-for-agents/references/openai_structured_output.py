"""
Reference: https://zhuanlan.zhihu.com/p/1931793563127100738
"""
import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel

# ignore env load and llm call

client_deepseek = OpenAI() # ignore params

client_qwen = OpenAI() # ignore params


# =========================
# Logit Bias
# =========================
def get_yes_no_answer_logit_bias(question: str) -> str:
    logit_bias = {
        'yes': 1000,
        'no': 1000,
    }

    response = client_deepseek.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": question}
        ],
        max_tokens=1,
        logit_bias=logit_bias,
        temperature=0.1
    )

    return response.choices[0].message.content.lower()


# =========================
# Response Format
# =========================
class Step(BaseModel):
    explanation: str
    output: str
    
class MathResponse(BaseModel):
    steps: list[Step]
    final_answer: str
    
def math_reasoning(question: str) -> str:

    response = client_qwen.chat.completions.parse(
        model="your-model-name",
        messages=[
            {"role": "user", "content": question}
        ],
        max_tokens=4096,
        temperature=0.1,
        response_format=MathResponse
    )

    return response.choices[0].message.content



if __name__ == "__main__":
    # Test - Logit Bias
    questions = [
        "Is water wet?",
        "Can birds fly?",
        "Is Python better than JavaScript?",
        "Is the sky green?"
    ]

    valid_answer = ['yes', 'no']

    for q in questions:
        answer = get_yes_no_answer_logit_bias(q)
        
        print(f"Raw answer:\n {answer}")
        
        if answer not in valid_answer:
            print(f"Q: {q}\nA: I dont't know\n")
        else:
            print(f"Q: {q}\nA: {answer}\n")

    # Test - Response Format
    math_question = "How to sovle 8x + 7 = -23?"
    math_response = math_reasoning(math_question)
    print(math_response)
    