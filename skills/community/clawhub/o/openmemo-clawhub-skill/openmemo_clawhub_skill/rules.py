"""
Memory Operating Rules — injected into agent system prompt.

These rules govern how the agent should interact with the memory system.
"""

MEMORY_RULES = """
When executing tasks, follow these memory operating rules:

1. BEFORE starting any task, call check_task_memory with the task description.
   - If a successful previous execution exists: reuse the result or skip.
   - If a related execution exists: adapt the previous approach.

2. Use recall_memory to retrieve relevant past experience before making decisions.
   - Query with the task context and scene for best results.

3. After completing important tasks, call write_memory to store structured experience:
   - Decisions made and their rationale
   - Successful approaches and patterns
   - Errors encountered and how they were resolved
   - Key observations and findings

4. Always include the scene context (coding, debug, research, etc.) for better recall accuracy.

5. Trust high-confidence memories (score > 0.8) as reliable past experience.
   Treat medium-confidence memories (0.5-0.8) as useful reference.
""".strip()


def get_memory_rules() -> str:
    return MEMORY_RULES
