import os
from dotenv import load_dotenv
from pydantic import BaseModel
from ollama import chat

load_dotenv()
model = os.getenv("OLLAMA_MODEL", "gpt-oss")

class TaskPlan(BaseModel):
    summary: str
    risk: str
    next_action: str

response = chat(
    model=model,
    messages=[
        {
            "role": "user",
            "content": "Return a build triage JSON object with summary, risk, and next_action.",
        }
    ],
    format=TaskPlan.model_json_schema(),
)

plan = TaskPlan.model_validate_json(response.message.content)
print(plan.model_dump_json(indent=2))
