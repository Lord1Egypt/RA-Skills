"""FastAPI entrypoint for cloud functions deployed to Railway / Supabase / generic.

Each registered function is exposed at POST /<name> and accepts a JSON body
that the function chooses to interpret. Add new functions in `functions/` and
register them in `registry.py`.
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from registry import EXPOSED_FUNCTIONS

app = FastAPI(title="n8n-evol-I cloud functions")


@app.get("/")
async def root() -> dict:
    return {"ok": True, "functions": sorted(EXPOSED_FUNCTIONS.keys())}


@app.post("/{name}")
async def call(name: str, request: Request) -> JSONResponse:
    fn = EXPOSED_FUNCTIONS.get(name)
    if fn is None:
        raise HTTPException(status_code=404, detail=f"unknown function: {name}")
    body = await request.json() if request.headers.get("content-type", "").startswith("application/json") else {}
    result = fn(body)
    return JSONResponse(result)
