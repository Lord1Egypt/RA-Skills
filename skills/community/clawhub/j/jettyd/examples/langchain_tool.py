"""
jettyd LangChain tool — wrap the jettyd REST API as LangChain tools.

Usage:
    pip install langchain langchain-openai requests

    export OPENAI_API_KEY=sk-...
    python langchain_tool.py
"""

import json
import os
from pathlib import Path
from typing import Optional

import requests
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


# ---------------------------------------------------------------------------
# Config helpers
# ---------------------------------------------------------------------------

def _load_api_key() -> str:
    """Load jettyd API key from openclaw.json or JETTYD_API_KEY env var."""
    env_key = os.environ.get("JETTYD_API_KEY")
    if env_key:
        return env_key

    config_path = Path.home() / ".openclaw" / "openclaw.json"
    if config_path.exists():
        config = json.loads(config_path.read_text())
        key = (
            config.get("skills", {})
            .get("entries", {})
            .get("jettyd", {})
            .get("apiKey")
        )
        if key:
            return key

    raise RuntimeError(
        "No jettyd API key found. Set JETTYD_API_KEY or add it to "
        "~/.openclaw/openclaw.json under skills.entries.jettyd.apiKey"
    )


BASE_URL = "https://api.jettyd.com/v1"
DEMO_DEVICE_ID = "930c4077-fbe7-48f2-824c-c9e806175f58"


def _headers() -> dict:
    return {"Authorization": f"Bearer {_load_api_key()}"}


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

class ListDevicesTool(BaseTool):
    name: str = "list_devices"
    description: str = (
        "List all jettyd IoT devices with their online/offline status and last-seen time. "
        "Returns a JSON list of device objects."
    )

    def _run(self, query: str = "") -> str:
        resp = requests.get(f"{BASE_URL}/devices", headers=_headers(), timeout=10)
        resp.raise_for_status()
        devices = resp.json()
        summary = [
            {
                "id": d.get("id"),
                "name": d.get("name"),
                "online": d.get("online", False),
                "lastSeen": d.get("lastSeen"),
            }
            for d in devices
        ]
        return json.dumps(summary, indent=2)


class ReadDeviceShadowTool(BaseTool):
    name: str = "read_device_shadow"
    description: str = (
        "Read the latest sensor readings (shadow) for a jettyd device. "
        "Input: a device ID string. "
        "Returns JSON with all current sensor values (temperature, humidity, voltage, etc.)."
    )

    def _run(self, device_id: str) -> str:
        device_id = device_id.strip()
        resp = requests.get(
            f"{BASE_URL}/devices/{device_id}/shadow",
            headers=_headers(),
            timeout=10,
        )
        resp.raise_for_status()
        return json.dumps(resp.json(), indent=2)


class SendCommandTool(BaseTool):
    name: str = "send_command"
    description: str = (
        "Send a command to a jettyd device. "
        'Input: JSON string with keys "device_id" (string), "action" (string), '
        'and optional "params" (object). '
        "Common actions: relay.on, relay.off, led.on, led.off, led.blink, led.toggle. "
        'Example: {"device_id": "abc123", "action": "relay.on", "params": {"duration": 5000}}'
    )

    def _run(self, input_json: str) -> str:
        try:
            data = json.loads(input_json)
        except json.JSONDecodeError as exc:
            return f"Invalid JSON input: {exc}"

        device_id = data.get("device_id", "").strip()
        if not device_id:
            return "Missing device_id"

        payload = {"action": data["action"]}
        if "params" in data:
            payload["params"] = data["params"]

        resp = requests.post(
            f"{BASE_URL}/devices/{device_id}/commands",
            headers={**_headers(), "Content-Type": "application/json"},
            json=payload,
            timeout=10,
        )
        resp.raise_for_status()
        return json.dumps(resp.json(), indent=2)


# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------

def build_agent(verbose: bool = True) -> AgentExecutor:
    tools = [ListDevicesTool(), ReadDeviceShadowTool(), SendCommandTool()]

    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful IoT assistant with access to jettyd device tools. "
                "Use them to answer questions about devices and sensor readings.",
            ),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    agent = create_openai_functions_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=verbose)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent_executor = build_agent()

    questions = [
        "What devices do I have and which are online?",
        f"What is the current temperature on device {DEMO_DEVICE_ID}?",
        f"Turn on the LED on device {DEMO_DEVICE_ID}.",
    ]

    for question in questions:
        print(f"\n>>> {question}")
        result = agent_executor.invoke({"input": question})
        print(result["output"])
