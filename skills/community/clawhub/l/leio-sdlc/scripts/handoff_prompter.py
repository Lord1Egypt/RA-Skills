from agent_driver import build_prompt

class HandoffPrompter:
    @classmethod
    def get_prompt(cls, condition: str) -> str:
        prompt = build_prompt(f"handoff_{condition}")
        if not prompt:
            return "[ACTION REQUIRED FOR MANAGER]\nUnknown exit condition."
        return prompt
