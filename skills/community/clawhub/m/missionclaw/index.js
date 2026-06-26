const MISSIONCLAW_URL = process.env.MISSIONCLAW_URL || "http://localhost:3000";

// Parse project details from user input
function parseProjectInput(input) {
  // Try to extract project name, description, type, and priority
  const parts = input.split(/ - |, /);
  
  const result = {
    projectName: parts[0]?.trim() || "Untitled Project",
    description: parts[0]?.trim() || "",
    projectType: "",
    priority: "medium"
  };
  
  // Look for keywords to determine project type
  const fullText = input.toLowerCase();
  
  if (fullText.includes("web") || fullText.includes("website") || fullText.includes("frontend") || fullText.includes("backend")) {
    result.projectType = "web development";
  } else if (fullText.includes("mobile") || fullText.includes("app") || fullText.includes("ios") || fullText.includes("android")) {
    result.projectType = "mobile development";
  } else if (fullText.includes("marketing") || fullText.includes("seo") || fullText.includes("ads") || fullText.includes("social media")) {
    result.projectType = "digital marketing";
  } else if (fullText.includes("design") || fullText.includes("logo") || fullText.includes("graphic")) {
    result.projectType = "creative design";
  }
  
  // Look for priority
  if (fullText.includes("high priority") || fullText.includes("urgent") || fullText.includes("asap")) {
    result.priority = "high";
  } else if (fullText.includes("low priority")) {
    result.priority = "low";
  }
  
  // Use remaining parts as description
  if (parts.length > 1) {
    result.description = parts.slice(1).join(" - ");
  }
  
  return result;
}

// Handle /mc command
async function handleMcCommand(args, context) {
  const subcommand = args[0]?.toLowerCase();
  
  if (!subcommand || subcommand === "help") {
    return {
      content: `**MissionClaw Commands:**

\`/mc create <project-details>\` - Create project in MissionClaw
\`/mc status <project-id>\` - Get project progress
\`/mc list\` - List all projects
\`/mc teams\` - List available teams

**Example:**
\`/mc create Build an e-commerce website with shopping cart - web development - high priority\``
    };
  }
  
  if (subcommand === "create") {
    const projectDetails = args.slice(1).join(" ");
    if (!projectDetails) {
      return { content: "Please provide project details. Example: `/mc create Build a marketing website - web development`" };
    }
    
    const parsed = parseProjectInput(projectDetails);
    
    try {
      const response = await fetch(`${MISSIONCLAW_URL}/api/projects`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(parsed)
      });
      
      const data = await response.json();
      
      if (data.success) {
        return {
          content: `**✅ Project Created in MissionClaw**

**Project:** ${data.project.name}
**Team:** ${data.project.team || "Unassigned"}
**Tasks Created:** ${data.tasksCreated}
**Message:** ${data.message}

**Project ID:** \`${data.project.id}\`

Use \`/mc status ${data.project.id}\` to check progress.`
        };
      } else {
        return { content: `**Error:** ${data.error}` };
      }
    } catch (error) {
      return { content: `**Connection Error:** Could not connect to MissionClaw at ${MISSIONCLAW_URL}. Make sure MissionClaw is running.` };
    }
  }
  
  if (subcommand === "status") {
    const projectId = args[1];
    if (!projectId) {
      return { content: "Please provide project ID. Example: `/mc status project-123`" };
    }
    
    try {
      const response = await fetch(`${MISSIONCLAW_URL}/api/projects?action=report&projectId=${projectId}`);
      const data = await response.json();
      
      if (data.projectName) {
        const progress = data.summary.progress;
        return {
          content: `**📊 Project Status: ${data.projectName}**

**Progress:** ${progress}%

- ✅ Completed: ${data.summary.completed}
- 🔄 In Progress: ${data.summary.inProgress}
- ⏳ Pending: ${data.summary.pending}

**${data.readyForReview ? "🎉 Project Complete - Ready for review!" : "Tasks in progress..."}**`
        };
      } else {
        return { content: "Project not found." };
      }
    } catch (error) {
      return { content: `**Connection Error:** Could not connect to MissionClaw.` };
    }
  }
  
  if (subcommand === "list") {
    try {
      const response = await fetch(`${MISSIONCLAW_URL}/api/projects`);
      const data = await response.json();
      
      if (data.projects.length === 0) {
        return { content: "No projects in MissionClaw yet." };
      }
      
      const projectList = data.projects.map(p => 
        `- **${p.name}** (${p.completedCount}/${p.taskCount} tasks) - \`${p.id}\``
      ).join("\n");
      
      return { content: `**📁 Projects in MissionClaw:**\n\n${projectList}` };
    } catch (error) {
      return { content: `**Connection Error:** Could not connect to MissionClaw.` };
    }
  }
  
  if (subcommand === "teams") {
    return {
      content: `**🏢 Available Teams in MissionClaw:**

- **Marketing** - Digital marketing, SEO, ads, content, social media
- **Developer** - Web, mobile, app, software development
- **Creative** - Design, graphics, video, UI/UX
- **Sales** - CRM, leads, client management
- **Support** - Helpdesk, bugs, issues
- **Operations** - Workflow, automation, integrations

Projects are automatically routed to the appropriate team based on keywords in the project description.`
    };
  }
  
  return { content: "Unknown command. Use `/mc help` for available commands." };
}

module.exports = {
  name: "missionclaw",
  handle: async (args, context) => {
    return handleMcCommand(args, context);
  }
};