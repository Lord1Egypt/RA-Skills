# open-langchain

A tiny browser skill that opens **LangChain** in Brave and takes the user directly to the builder/dashboard by clicking **Start building**.

## What it does

1. Opens `https://www.langchain.com/`
2. Finds the main **Start building** button
3. Clicks it
4. Waits for the destination to load
5. Verifies that the LangChain/LangSmith builder or dashboard is visible

## Trigger examples

```text
Open LangChain
Open LangChain and start building
Take me to the LangChain dashboard
Start building with LangChain
Go to LangChain's builder
```

## Browser

Designed for Brave browser automation.

The skill uses the visible **Start building** UI rather than hard-coding a dashboard URL, making it more resilient to destination URL changes.

## Authentication

If LangChain/LangSmith asks the user to sign in, the skill stops at the login page. It never handles or stores credentials.

## Installation

Place this directory in your OpenClaw skills directory:

```text
skills/open-langchain/
```

Required file:

```text
SKILL.md
```

## Configuration

`config.yaml` contains the public homepage and UI behavior. No API keys are required.

## License

MIT
