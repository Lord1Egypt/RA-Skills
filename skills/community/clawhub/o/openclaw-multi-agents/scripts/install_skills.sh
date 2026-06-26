#!/bin/bash
# install_skills.sh - 为子Agent安装skills
# 版本: 5.0.2 (修复：统一使用clawhub，修正workspace路径)

set -e

AGENT_NAME=$1
AGENT_DIR=~/.openclaw/workspace-$AGENT_NAME
SKILLS_DIR=$AGENT_DIR/skills

if [ -z "$AGENT_NAME" ]; then
    echo "Usage: $0 <agent_name>"
    echo "Example: $0 munger"
    exit 1
fi

if [ ! -d "$AGENT_DIR" ]; then
    echo "❌ Agent workspace not found: $AGENT_DIR"
    echo "Run: bash create_agent.sh $AGENT_NAME"
    exit 1
fi

echo "📦 Installing skills for: $AGENT_NAME"
echo "   Skills来源: https://claw123.ai"

case $AGENT_NAME in
  munger)
    echo "Installing strategic planning skills..."
    cd $SKILLS_DIR
    clawhub install product-research || echo "⚠️ product-research failed"
    clawhub install brainstorming || echo "⚠️ brainstorming failed"
    clawhub install deep-reading-analyst || echo "⚠️ deep-reading-analyst failed"
    ;;
  
  feynman)
    echo "Installing development skills..."
    cd $SKILLS_DIR
    clawhub install senior-fullstack || echo "⚠️ senior-fullstack failed"
    clawhub install systematic-debugging || echo "⚠️ systematic-debugging failed"
    clawhub install github || echo "⚠️ github failed"
    ;;
  
  deming)
    echo "Installing quality assurance skills..."
    cd $SKILLS_DIR
    clawhub install code-review-excellence || echo "⚠️ code-review-excellence failed"
    clawhub install e2e-testing-patterns || echo "⚠️ e2e-testing-patterns failed"
    ;;
  
  drucker)
    echo "Installing project management skills..."
    cd $SKILLS_DIR
    clawhub install project-manager || echo "⚠️ project-manager failed"
    clawhub install doc-coauthoring || echo "⚠️ doc-coauthoring failed"
    ;;
  
  kahneman)
    echo "Installing data analysis skills..."
    cd $SKILLS_DIR
    clawhub install data-visualization || echo "⚠️ data-visualization failed"
    ;;
  
  jobs)
    echo "Installing content creation skills..."
    cd $SKILLS_DIR
    clawhub install copywriting || echo "⚠️ copywriting failed"
    clawhub install copy-editing || echo "⚠️ copy-editing failed"
    clawhub install frontend-design || echo "⚠️ frontend-design failed"
    ;;
  
  kuaishou|scholar|sentinel)
    echo "Tool-type agent: no additional skills needed"
    ;;
  
  *)
    echo "Unknown agent type: $AGENT_NAME"
    echo "Please manually install skills:"
    echo "  cd $SKILLS_DIR"
    echo "  clawhub install <skill-name>"
    echo ""
    echo "Find skills at: https://claw123.ai"
    exit 1
    ;;
esac

echo ""
echo "✅ Skills installation completed"
echo "Installed skills:"
ls -la $SKILLS_DIR | grep -v "^total" | grep -v "^\." || echo "  (none)"