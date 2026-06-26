# server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
from transformers import MT5ForConditionalGeneration, T5Tokenizer
import uvicorn

app = FastAPI()

MODEL_NAME = "heack/HeackMT5-ZhSum100k"
print("⏳ 正在将 HeackMT5 载入内存，请稍候...")

# 全局加载模型，保证只加载一次
tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
model = MT5ForConditionalGeneration.from_pretrained(MODEL_NAME)

if torch.cuda.is_available():
    device = torch.device("cuda")
elif torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")
model.to(device)

print(f"✅ 模型已成功加载至 {device}，随时待命！")

class SummaryRequest(BaseModel):
    text: str
    length: int = 150

def _split_text(text, length=300):
    # (保留我们上一步写好的完美的断句逻辑...)
    chunks = []
    start = 0
    punctuations = {'.', '。', '，', ','}
    while start < len(text):
        if len(text) - start <= length:
            chunks.append(text[start:])
            break
        target_pos = start + length
        pos = target_pos
        for offset in range(21):
            pos_backward = target_pos - offset
            pos_forward = target_pos + offset
            if pos_backward > start and text[pos_backward] in punctuations:
                pos = pos_backward
                break
            if pos_forward < len(text) and text[pos_forward] in punctuations:
                pos = pos_forward
                break
        chunks.append(text[start:pos+1])
        start = pos + 1
    if len(chunks) > 1 and len(chunks[-1]) < 100:
        chunks[-2] += chunks[-1]
        chunks.pop()
    return chunks

@app.get("/health")
def health_check():
    return {"status": "alive"}

@app.post("/summarize")
def summarize(req: SummaryRequest):
    try:
        chunks = _split_text(req.text, 300)
        summaries = []
        for chunk in chunks:
            inputs = tokenizer(
                "summarize: " + chunk, 
                return_tensors='pt', 
                max_length=512, 
                truncation=True
            ).to(device)
            
            summary_ids = model.generate(
                **inputs,
                max_length=req.length, 
                num_beams=4, 
                length_penalty=1.5, 
                no_repeat_ngram_size=2
            )
            summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            summaries.append(summary)
            
        return {"result": "\n".join([f"• {s}" for s in summaries])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # 绑定在本地特定端口，不与别人冲突
    uvicorn.run(app, host="127.0.0.1", port=28199)