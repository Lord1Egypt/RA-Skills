# LoR (Loop of Resilience)

A robust, modular verification system for OpenClaw. 

The LoR system forces the agent into a 5-step diagnostic process, ensuring high-quality outputs for complex tasks and preventing hallucinations through automated verification. It implements a Chain of Thought (CoT) paradigm to enhance agent reliability.

## Architecture
```text
lor-skill/
├── engine/          # Verification Logic (Modular)
├── tests/           # Automated Verification Tests
├── scripts/         # Installation & Lifecycle Hooks
└── package.json     # Node.js dependencies
```

## GitHub Repository
- [https://github.com/lumi77-mac/lor-skill](https://github.com/lumi77-mac/lor-skill)

## Installation
1. Clone this repository into your `skills/` directory:
   ```bash
   git clone https://github.com/lumi77-mac/lor-skill.git
   ```
2. Run the setup script:
   ```bash
   ./scripts/setup.sh
   ```

## Usage
`@[AgentName] /lor [task]` to trigger the verification loop.

## The LoR (Chain of Thought) Process
1. **Raw Reply**: Initial model output.
2. **Plan Verifications**: Decomposition & Tool Planning.
3. **Execute Verification**: Forced Tool Execution (with safety checks).
4. **Checking Results**: Validation loop (max 3 retries).
5. **Final Result**: Concise summary output.

## Keywords
Chain of Thought, CoT, Verification, Resilience, Reliability, Automation, Agent Diagnostic
