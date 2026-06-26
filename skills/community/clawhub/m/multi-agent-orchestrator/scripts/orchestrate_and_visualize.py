
import json
import subprocess
from generate_agents import generate_agents
from visualize_collaboration import generate_org_chart_mermaid, generate_swimlane_mermaid

def orchestrate_and_visualize(prompt: str, output_dir: str = "."):
    """
    Orchestrates agent generation and visualization.
    Generates agents based on a prompt, creates Mermaid diagrams, and renders them to PNG.
    """
    print(f"Generating agents for prompt: {prompt}")
    agent_data = generate_agents(prompt)
    agents = agent_data["agents"]
    collaboration_model = agent_data["collaboration_model"]

    print("Generating organizational chart Mermaid code...")
    org_chart_mermaid = generate_org_chart_mermaid(agents)
    org_chart_mermaid_path = f"{output_dir}/org_chart.mmd"
    with open(org_chart_mermaid_path, "w") as f:
        f.write(org_chart_mermaid)
    print(f"Organizational chart Mermaid code saved to {org_chart_mermaid_path}")

    print("Rendering organizational chart to PNG...")
    org_chart_png_path = f"{output_dir}/org_chart.png"
    try:
        subprocess.run(["manus-render-diagram", org_chart_mermaid_path, org_chart_png_path], check=True)
        print(f"Organizational chart rendered to {org_chart_png_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error rendering organizational chart: {e}")
        print("Please ensure 'manus-render-diagram' is installed and accessible.")
        org_chart_png_path = None

    print("Generating swimlane diagram Mermaid code...")
    swimlane_mermaid = generate_swimlane_mermaid(agents, collaboration_model)
    swimlane_mermaid_path = f"{output_dir}/swimlane.mmd"
    with open(swimlane_mermaid_path, "w") as f:
        f.write(swimlane_mermaid)
    print(f"Swimlane diagram Mermaid code saved to {swimlane_mermaid_path}")

    print("Rendering swimlane diagram to PNG...")
    swimlane_png_path = f"{output_dir}/swimlane.png"
    try:
        subprocess.run(["manus-render-diagram", swimlane_mermaid_path, swimlane_png_path], check=True)
        print(f"Swimlane diagram rendered to {swimlane_png_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error rendering swimlane diagram: {e}")
        print("Please ensure 'manus-render-diagram' is installed and accessible.")
        swimlane_png_path = None

    return {
        "agents": agents,
        "collaboration_model": collaboration_model,
        "org_chart_mermaid": org_chart_mermaid_path,
        "org_chart_png": org_chart_png_path,
        "swimlane_mermaid": swimlane_mermaid_path,
        "swimlane_png": swimlane_png_path,
    }

if __name__ == "__main__":
    # Example usage
    output_directory = "/home/ubuntu/multi_agent_orchestrator_output"
    subprocess.run(["mkdir", "-p", output_directory], check=True)

    print("\n--- Orchestrating Software Development Team ---")
    sd_results = orchestrate_and_visualize("Create a software development team for an e-commerce platform.", output_directory)
    print(json.dumps(sd_results, indent=2))

    print("\n--- Orchestrating Market Research Team ---")
    mr_results = orchestrate_and_visualize("Conduct market research for a new AI product.", output_directory)
    print(json.dumps(mr_results, indent=2))
