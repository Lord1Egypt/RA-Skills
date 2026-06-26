from scripts.prompt_optimizer import PromptOptimizer, PromptLibrary

def demo_analysis():
    optimizer = PromptOptimizer()
    
    prompts = [
        "Write a story about a robot",
        "You are an expert Python developer. Write a function to parse JSON data with error handling and logging. Include type hints and docstrings.",
        "Translate the following text to French: 'Hello world'",
    ]
    
    for prompt in prompts:
        print(f"\n{'='*60}")
        print(f"Original: {prompt}")
        analysis = optimizer.analyze(prompt)
        print(f"Score: {analysis['overall_score']}/10")
        print(f"Suggestions: {optimizer.suggest_improvements(prompt)}")
        optimized = optimizer.optimize(prompt)
        print(f"Optimized: {optimized[:200]}...")


def demo_templates():
    optimizer = PromptOptimizer()
    
    print("\n=== Template Examples ===")
    
    cot = optimizer.apply_template(
        "chain_of_thought",
        task="calculate the factorial of 5"
    )
    print(f"Chain-of-Thought: {cot}\n")
    
    few_shot = optimizer.apply_template(
        "few_shot",
        examples="Q: 2+2=? A: 4\nQ: 3+5=? A: 8",
        task="Q: 7+3=?"
    )
    print(f"Few-shot: {few_shot}\n")
    
    role = optimizer.apply_template(
        "role_playing",
        domain="medical research",
        task="Summarize the latest findings on mRNA vaccines"
    )
    print(f"Role-playing: {role}\n")


def demo_library():
    lib = PromptLibrary("demo_prompts.json")
    
    lib.save(
        "python-coding",
        "You are a senior Python developer. Write clean, PEP8-compliant code.",
        tags=["coding", "python"]
    )
    lib.save(
        "essay-writing",
        "You are an academic writing expert. Write a well-structured essay.",
        tags=["writing", "academic"]
    )
    
    print(f"All prompts: {lib.list_all()}")
    print(f"Coding prompts: {lib.search('coding')}")
    print(f"Get 'python-coding': {lib.get('python-coding')[:50]}...")
    
    # cleanup
    import os
    if os.path.exists("demo_prompts.json"):
        os.remove("demo_prompts.json")


if __name__ == "__main__":
    demo_analysis()
    demo_templates()
    demo_library()
