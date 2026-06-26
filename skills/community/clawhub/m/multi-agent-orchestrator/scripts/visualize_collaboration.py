
import json

def generate_org_chart_mermaid(agents: dict) -> str:
    """
    Generates a Mermaid organizational chart for the given agents.
    """
    mermaid_code = "graph TD\n"
    for agent_id, agent_data in agents.items():
        mermaid_code += f"    {agent_id}[\"{agent_data['role']}\"]\n"
    return mermaid_code

def generate_swimlane_mermaid(agents: dict, collaboration_model: str) -> str:
    """
    Generates a Mermaid swimlane diagram for the given agents and collaboration model.
    This is a simplified representation.
    """
    mermaid_code = "graph LR\n"
    mermaid_code += "    subgraph Collaboration Workflow\n"

    if collaboration_model == "vertical":
        # Assuming a simple hierarchy for vertical: PM -> Devs -> QA/Auditor
        pm_agent = next((id for id, data in agents.items() if "product manager" in data['role'].lower()), None)
        dev_agents = [id for id, data in agents.items() if "developer" in data['role'].lower()]
        qa_auditor_agents = [id for id, data in agents.items() if "qa" in data['role'].lower() or "auditor" in data['role'].lower()]

        if pm_agent:
            mermaid_code += f"        subgraph {agents[pm_agent]['role']}\n"
            mermaid_code += f"            {pm_agent}[\"{agents[pm_agent]['role']}\"]\n"
            mermaid_code += f"        end\n"

        if dev_agents:
            mermaid_code += f"        subgraph Development\n"
            for dev_agent in dev_agents:
                mermaid_code += f"            {dev_agent}[\"{agents[dev_agent]['role']}\"]\n"
            mermaid_code += f"        end\n"

        if qa_auditor_agents:
            mermaid_code += f"        subgraph Quality Assurance & Security\n"
            for qa_agent in qa_auditor_agents:
                mermaid_code += f"            {qa_agent}[\"{agents[qa_agent]['role']}\"]\n"
            mermaid_code += f"        end\n"

        # Add links for vertical flow
        if pm_agent and dev_agents:
            for dev_agent in dev_agents:
                mermaid_code += f"        {pm_agent} --> {dev_agent}\n"
        if dev_agents and qa_auditor_agents:
            for dev_agent in dev_agents:
                for qa_agent in qa_auditor_agents:
                    mermaid_code += f"        {dev_agent} --> {qa_agent}\n"

    elif collaboration_model == "horizontal":
        # For horizontal, all agents are peers and interact with each other
        agent_ids = list(agents.keys())
        for i in range(len(agent_ids)):
            mermaid_code += f"        subgraph {agents[agent_ids[i]]['role']}\n"
            mermaid_code += f"            {agent_ids[i]}[\"{agents[agent_ids[i]]['role']}\"]\n"
            mermaid_code += f"        end\n"
            for j in range(i + 1, len(agent_ids)):
                mermaid_code += f"        {agent_ids[i]} <--> {agent_ids[j]}\n"
    else:
        # Default for ad-hoc or unknown models
        for agent_id, agent_data in agents.items():
            mermaid_code += f"        subgraph {agent_data['role']}\n"
            mermaid_code += f"            {agent_id}[\"{agent_data['role']}\"]\n"
            mermaid_code += f"        end\n"

    mermaid_code += "    end\n"
    return mermaid_code

if __name__ == "__main__":
    # Example usage with dummy data from generate_agents.py
    from generate_agents import generate_agents

    print("\n--- Software Development Org Chart ---")
    sd_result = generate_agents("software development")
    print(generate_org_chart_mermaid(sd_result["agents"]))

    print("\n--- Software Development Swimlane ---")
    print(generate_swimlane_mermaid(sd_result["agents"], sd_result["collaboration_model"]))

    print("\n--- Market Research Org Chart ---")
    mr_result = generate_agents("market research")
    print(generate_org_chart_mermaid(mr_result["agents"]))

    print("\n--- Market Research Swimlane ---")
    print(generate_swimlane_mermaid(mr_result["agents"], mr_result["collaboration_model"]))
