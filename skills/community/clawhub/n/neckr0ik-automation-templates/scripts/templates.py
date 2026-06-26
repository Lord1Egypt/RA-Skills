#!/usr/bin/env python3
"""
Automation Templates - Ready-to-use workflow templates for n8n, Make, Zapier

Usage:
    python templates.py list
    python templates.py get --name email-drip-campaign --platform n8n
    python templates.py search --keyword email
    python templates.py generate --template lead-capture --output ./workflow.json
"""

import os
import sys
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class AutomationTemplate:
    """Represents an automation template."""
    
    name: str
    platform: str  # n8n, make, zapier
    category: str  # email, crm, data, notification, ecommerce
    description: str
    trigger: Dict
    nodes: List[Dict]
    connections: Dict
    settings: Dict = field(default_factory=dict)
    variables: Dict[str, str] = field(default_factory=dict)
    docs: str = ""


# Template Library
TEMPLATES = {
    # Email & Marketing
    "email-drip-campaign": AutomationTemplate(
        name="email-drip-campaign",
        platform="n8n",
        category="email",
        description="Multi-email sequence with delays",
        trigger={
            "type": "webhook",
            "name": "Webhook Trigger",
            "parameters": {"path": "email-drip", "method": "POST"}
        },
        nodes=[
            {"type": "webhook", "name": "Webhook", "position": [250, 300]},
            {"type": "httpRequest", "name": "Add to List", "position": [450, 300]},
            {"type": "wait", "name": "Wait 1 Day", "position": [650, 300]},
            {"type": "httpRequest", "name": "Send Email 1", "position": [850, 300]},
            {"type": "wait", "name": "Wait 3 Days", "position": [1050, 300]},
            {"type": "httpRequest", "name": "Send Email 2", "position": [1250, 300]},
            {"type": "wait", "name": "Wait 5 Days", "position": [1450, 300]},
            {"type": "httpRequest", "name": "Send Email 3", "position": [1650, 300]},
        ],
        connections={
            "Webhook": {"main": [[{"node": "Add to List", "type": "main"}]]},
            "Add to List": {"main": [[{"node": "Wait 1 Day", "type": "main"}]]},
            "Wait 1 Day": {"main": [[{"node": "Send Email 1", "type": "main"}]]},
            "Send Email 1": {"main": [[{"node": "Wait 3 Days", "type": "main"}]]},
            "Wait 3 Days": {"main": [[{"node": "Send Email 2", "type": "main"}]]},
            "Send Email 2": {"main": [[{"node": "Wait 5 Days", "type": "main"}]]},
            "Wait 5 Days": {"main": [[{"node": "Send Email 3", "type": "main"}]]},
        },
        settings={
            "timezone": "UTC",
            "saveExecutionProgress": True,
            "saveStaticData": False
        },
        variables={
            "EMAIL_API_KEY": "Your email provider API key",
            "LIST_ID": "Your email list ID",
            "EMAIL_1_SUBJECT": "Welcome to our service!",
            "EMAIL_2_SUBJECT": "Here's what you missed...",
            "EMAIL_3_SUBJECT": "Last chance!"
        },
        docs="1. Configure webhook URL\n2. Add your email provider credentials\n3. Customize email subjects and content\n4. Activate workflow"
    ),
    
    "newsletter-signup": AutomationTemplate(
        name="newsletter-signup",
        platform="n8n",
        category="email",
        description="Add to list + welcome email",
        trigger={
            "type": "webhook",
            "name": "Form Submission",
            "parameters": {"path": "newsletter", "method": "POST"}
        },
        nodes=[
            {"type": "webhook", "name": "Webhook", "position": [250, 300]},
            {"type": "httpRequest", "name": "Add to Email List", "position": [450, 300]},
            {"type": "httpRequest", "name": "Send Welcome Email", "position": [650, 300]},
            {"type": "respondToWebhook", "name": "Respond", "position": [850, 300]},
        ],
        connections={
            "Webhook": {"main": [[{"node": "Add to Email List", "type": "main"}]]},
            "Add to Email List": {"main": [[{"node": "Send Welcome Email", "type": "main"}]]},
            "Send Welcome Email": {"main": [[{"node": "Respond", "type": "main"}]]},
        },
        settings={"timezone": "UTC"},
        variables={
            "EMAIL_PROVIDER": "sendgrid|mailchimp|postmark",
            "API_KEY": "Your API key",
            "LIST_ID": "Your list ID",
            "WELCOME_SUBJECT": "Welcome!",
            "WELCOME_BODY": "Thanks for signing up..."
        },
        docs="1. Set webhook URL in your form\n2. Configure email provider\n3. Customize welcome email\n4. Activate"
    ),
    
    "lead-capture": AutomationTemplate(
        name="lead-capture",
        platform="make",
        category="crm",
        description="Form → CRM → Email sequence",
        trigger={
            "type": "webhook",
            "name": "Webhook",
            "parameters": {"path": "lead-capture"}
        },
        nodes=[
            {"type": "webhook", "name": "Webhook", "position": [100, 100]},
            {"type": "airtable", "name": "Add to Airtable", "position": [300, 100]},
            {"type": "slack", "name": "Notify Team", "position": [500, 100]},
            {"type": "email", "name": "Send Welcome", "position": [500, 300]},
        ],
        connections={
            "Webhook": [1, 2],
            "Add to Airtable": [2],
        },
        settings={},
        variables={
            "AIRTABLE_API_KEY": "Your Airtable API key",
            "AIRTABLE_BASE": "Your base ID",
            "SLACK_WEBHOOK": "Your Slack webhook",
            "EMAIL_API_KEY": "Your email API key"
        },
        docs="1. Create Airtable base with leads table\n2. Add Make webhook to your form\n3. Configure Slack webhook\n4. Set up email provider\n5. Activate"
    ),
    
    "webhook-to-slack": AutomationTemplate(
        name="webhook-to-slack",
        platform="n8n",
        category="notification",
        description="Webhook notifications to Slack",
        trigger={
            "type": "webhook",
            "name": "Webhook",
            "parameters": {"path": "notify", "method": "POST"}
        },
        nodes=[
            {"type": "webhook", "name": "Webhook", "position": [250, 300]},
            {"type": "slack", "name": "Send to Slack", "position": [450, 300]},
            {"type": "respondToWebhook", "name": "Respond", "position": [650, 300]},
        ],
        connections={
            "Webhook": {"main": [[{"node": "Send to Slack", "type": "main"}]]},
            "Send to Slack": {"main": [[{"node": "Respond", "type": "main"}]]},
        },
        settings={},
        variables={
            "SLACK_WEBHOOK_URL": "Your Slack webhook URL",
            "CHANNEL": "#notifications",
            "USERNAME": "Bot"
        },
        docs="1. Create Slack webhook\n2. Configure webhook URL in n8n\n3. Customize message format\n4. Activate"
    ),
    
    "daily-report": AutomationTemplate(
        name="daily-report",
        platform="n8n",
        category="notification",
        description="Scheduled summary reports",
        trigger={
            "type": "schedule",
            "name": "Daily Trigger",
            "parameters": {"rule": {"interval": [{"field": "hours", "hours": 9}]}}
        },
        nodes=[
            {"type": "scheduleTrigger", "name": "Daily 9am", "position": [250, 300]},
            {"type": "googleSheets", "name": "Get Data", "position": [450, 300]},
            {"type": "set", "name": "Format Report", "position": [650, 300]},
            {"type": "email", "name": "Send Email", "position": [850, 300]},
        ],
        connections={
            "Daily 9am": {"main": [[{"node": "Get Data", "type": "main"}]]},
            "Get Data": {"main": [[{"node": "Format Report", "type": "main"}]]},
            "Format Report": {"main": [[{"node": "Send Email", "type": "main"}]]},
        },
        settings={"timezone": "UTC"},
        variables={
            "SHEET_ID": "Your Google Sheet ID",
            "EMAIL_TO": "team@company.com",
            "EMAIL_SUBJECT": "Daily Report"
        },
        docs="1. Connect Google Sheets\n2. Configure data range\n3. Set email recipients\n4. Schedule time\n5. Activate"
    ),
    
    "sheets-to-database": AutomationTemplate(
        name="sheets-to-database",
        platform="n8n",
        category="data",
        description="Google Sheets → Airtable/Notion sync",
        trigger={
            "type": "schedule",
            "name": "Hourly Sync",
            "parameters": {"rule": {"interval": [{"field": "hours"}]}}
        },
        nodes=[
            {"type": "scheduleTrigger", "name": "Every Hour", "position": [250, 300]},
            {"type": "googleSheets", "name": "Read Sheets", "position": [450, 300]},
            {"type": "httpRequest", "name": "Write to Airtable", "position": [650, 300]},
        ],
        connections={
            "Every Hour": {"main": [[{"node": "Read Sheets", "type": "main"}]]},
            "Read Sheets": {"main": [[{"node": "Write to Airtable", "type": "main"}]]},
        },
        settings={},
        variables={
            "GOOGLE_SHEETS_ID": "Your Sheet ID",
            "AIRTABLE_API_KEY": "Your Airtable API key",
            "AIRTABLE_BASE": "Your Base ID"
        },
        docs="1. Connect Google Sheets\n2. Configure Airtable\n3. Map columns\n4. Set sync interval\n5. Activate"
    ),
    
    "error-alert": AutomationTemplate(
        name="error-alert",
        platform="n8n",
        category="notification",
        description="Error notifications to Slack/Email",
        trigger={
            "type": "errorTrigger",
            "name": "Error Trigger",
            "parameters": {}
        },
        nodes=[
            {"type": "errorTrigger", "name": "On Error", "position": [250, 300]},
            {"type": "slack", "name": "Alert Slack", "position": [450, 300]},
            {"type": "email", "name": "Alert Email", "position": [450, 500]},
        ],
        connections={
            "On Error": {"main": [[{"node": "Alert Slack", "type": "main"}, {"node": "Alert Email", "type": "main"}]]},
        },
        settings={},
        variables={
            "SLACK_WEBHOOK": "Your Slack webhook",
            "EMAIL_TO": "alerts@company.com"
        },
        docs="1. Configure Slack webhook\n2. Add email recipients\n3. Set as error handler for workflows\n4. Activate"
    ),
    
    "order-confirmation": AutomationTemplate(
        name="order-confirmation",
        platform="n8n",
        category="ecommerce",
        description="Order → Email → CRM",
        trigger={
            "type": "webhook",
            "name": "Order Webhook",
            "parameters": {"path": "order", "method": "POST"}
        },
        nodes=[
            {"type": "webhook", "name": "Order Webhook", "position": [250, 300]},
            {"type": "httpRequest", "name": "Add to CRM", "position": [450, 300]},
            {"type": "email", "name": "Send Confirmation", "position": [650, 300]},
            {"type": "slack", "name": "Notify Team", "position": [650, 500]},
        ],
        connections={
            "Order Webhook": {"main": [[{"node": "Add to CRM", "type": "main"}]]},
            "Add to CRM": {"main": [[{"node": "Send Confirmation", "type": "main"}, {"node": "Notify Team", "type": "main"}]]},
        },
        settings={},
        variables={
            "CRM_API_KEY": "Your CRM API key",
            "EMAIL_API_KEY": "Your email API key",
            "SLACK_WEBHOOK": "Your Slack webhook"
        },
        docs="1. Configure webhook in your store\n2. Set up CRM connection\n3. Customize confirmation email\n4. Activate"
    ),
    
    "customer-onboarding": AutomationTemplate(
        name="customer-onboarding",
        platform="n8n",
        category="ecommerce",
        description="Welcome sequence for new customers",
        trigger={
            "type": "webhook",
            "name": "New Customer",
            "parameters": {"path": "new-customer", "method": "POST"}
        },
        nodes=[
            {"type": "webhook", "name": "Webhook", "position": [250, 300]},
            {"type": "httpRequest", "name": "Add to CRM", "position": [450, 300]},
            {"type": "email", "name": "Welcome Email", "position": [650, 300]},
            {"type": "wait", "name": "Wait 1 Day", "position": [850, 300]},
            {"type": "email", "name": "Onboarding Email", "position": [1050, 300]},
            {"type": "wait", "name": "Wait 3 Days", "position": [1250, 300]},
            {"type": "email", "name": "Tips Email", "position": [1450, 300]},
        ],
        connections={
            "Webhook": {"main": [[{"node": "Add to CRM", "type": "main"}]]},
            "Add to CRM": {"main": [[{"node": "Welcome Email", "type": "main"}]]},
            "Welcome Email": {"main": [[{"node": "Wait 1 Day", "type": "main"}]]},
            "Wait 1 Day": {"main": [[{"node": "Onboarding Email", "type": "main"}]]},
            "Onboarding Email": {"main": [[{"node": "Wait 3 Days", "type": "main"}]]},
            "Wait 3 Days": {"main": [[{"node": "Tips Email", "type": "main"}]]},
        },
        settings={"timezone": "UTC"},
        variables={
            "CRM_API_KEY": "Your CRM API key",
            "EMAIL_API_KEY": "Your email API key",
            "WELCOME_SUBJECT": "Welcome!",
            "ONBOARDING_SUBJECT": "Getting Started",
            "TIPS_SUBJECT": "Pro Tips"
        },
        docs="1. Configure webhook\n2. Set up CRM\n3. Customize email sequence\n4. Activate"
    ),
}


class TemplateManager:
    """Manage automation templates."""
    
    def __init__(self, output_dir: str = "."):
        self.output_dir = Path(output_dir)
        self.templates = TEMPLATES
    
    def list_templates(self, category: Optional[str] = None,
                       platform: Optional[str] = None) -> List[Dict]:
        """List available templates."""
        
        results = []
        
        for name, template in self.templates.items():
            if category and template.category != category:
                continue
            if platform and template.platform != platform:
                continue
            
            results.append({
                "name": template.name,
                "platform": template.platform,
                "category": template.category,
                "description": template.description,
            })
        
        return results
    
    def get_template(self, name: str, platform: Optional[str] = None) -> Optional[Dict]:
        """Get a specific template."""
        
        # Try exact match first
        if name in self.templates:
            template = self.templates[name]
            if platform and template.platform != platform:
                # Try to adapt
                return self._adapt_template(template, platform)
            return template.__dict__
        
        # Try partial match
        for tname, template in self.templates.items():
            if name.lower() in tname.lower():
                if platform and template.platform != platform:
                    return self._adapt_template(template, platform)
                return template.__dict__
        
        return None
    
    def _adapt_template(self, template: AutomationTemplate, target_platform: str) -> Dict:
        """Adapt template to different platform."""
        
        # Basic adaptation - in real implementation would be more sophisticated
        adapted = template.__dict__.copy()
        adapted["platform"] = target_platform
        adapted["name"] = f"{template.name}-{target_platform}"
        adapted["docs"] = f"Adapted from {template.platform} to {target_platform}. May require manual adjustments."
        return adapted
    
    def search_templates(self, keyword: str,
                        platform: Optional[str] = None,
                        category: Optional[str] = None) -> List[Dict]:
        """Search templates by keyword."""
        
        results = []
        keyword_lower = keyword.lower()
        
        for name, template in self.templates.items():
            if keyword_lower in name.lower() or keyword_lower in template.description.lower():
                if category and template.category != category:
                    continue
                if platform and template.platform != platform:
                    continue
                
                results.append({
                    "name": template.name,
                    "platform": template.platform,
                    "category": template.category,
                    "description": template.description,
                })
        
        return results
    
    def generate_workflow(self, name: str, variables: Optional[Dict] = None,
                         output_format: str = "json") -> str:
        """Generate workflow from template."""
        
        template_data = self.get_template(name)
        if not template_data:
            raise ValueError(f"Template not found: {name}")
        
        template = AutomationTemplate(**template_data)
        
        # Apply variables
        if variables:
            template.variables.update(variables)
        
        # Generate platform-specific workflow
        if template.platform == "n8n":
            return self._generate_n8n(template, output_format)
        elif template.platform == "make":
            return self._generate_make(template, output_format)
        elif template.platform == "zapier":
            return self._generate_zapier(template, output_format)
        else:
            return json.dumps(template.__dict__, indent=2)
    
    def _generate_n8n(self, template: AutomationTemplate, output_format: str) -> str:
        """Generate n8n workflow JSON."""
        
        workflow = {
            "name": template.name,
            "nodes": template.nodes,
            "connections": template.connections,
            "active": False,
            "settings": template.settings,
            "versionId": "",
            "staticData": None,
            "tags": [],
            "triggerCount": 1,
            "updatedAt": datetime.now().isoformat(),
            "createdAt": datetime.now().isoformat(),
        }
        
        # Add variables as credentials placeholder
        workflow["credentials"] = {}
        for var_name, var_value in template.variables.items():
            workflow["credentials"][var_name] = {"value": f"{{{var_name}}}"}
        
        if output_format == "yaml":
            return yaml.dump(workflow, default_flow_style=False)
        return json.dumps(workflow, indent=2)
    
    def _generate_make(self, template: AutomationTemplate, output_format: str) -> str:
        """Generate Make.com scenario JSON."""
        
        scenario = {
            "name": template.name,
            "isPaused": True,
            "flow": [
                {
                    "id": i,
                    "module": node.get("type", "unknown"),
                    "version": 1,
                    "parameters": {},
                    "mapper": {},
                }
                for i, node in enumerate(template.nodes)
            ],
            "metadata": {
                "instant": False,
                "version": 1,
                "scenario": {
                    "roundtrips": 1,
                    "maxRounds": 3,
                },
            },
        }
        
        if output_format == "yaml":
            return yaml.dump(scenario, default_flow_style=False)
        return json.dumps(scenario, indent=2)
    
    def _generate_zapier(self, template: AutomationTemplate, output_format: str) -> str:
        """Generate Zapier zap definition."""
        
        zap = {
            "name": template.name,
            "trigger": {
                "app": "webhooks",
                "event": "catch_hook",
            },
            "steps": [
                {
                    "app": node.get("type", "unknown"),
                    "action": "action",
                    "params": {},
                }
                for node in template.nodes[1:]  # Skip trigger
            ],
            "variables": template.variables,
        }
        
        if output_format == "yaml":
            return yaml.dump(zap, default_flow_style=False)
        return json.dumps(zap, indent=2)


def main():
    """CLI entry point."""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="Automation Templates")
    subparsers = parser.add_subparsers(dest='command', help='Command')
    
    # list command
    list_parser = subparsers.add_parser('list', help='List templates')
    list_parser.add_argument('--category', help='Filter by category')
    list_parser.add_argument('--platform', help='Filter by platform')
    
    # get command
    get_parser = subparsers.add_parser('get', help='Get template')
    get_parser.add_argument('--name', required=True, help='Template name')
    get_parser.add_argument('--platform', help='Target platform')
    get_parser.add_argument('--output', help='Output file')
    get_parser.add_argument('--format', choices=['json', 'yaml'], default='json')
    
    # search command
    search_parser = subparsers.add_parser('search', help='Search templates')
    search_parser.add_argument('--keyword', required=True, help='Search keyword')
    search_parser.add_argument('--platform', help='Filter by platform')
    search_parser.add_argument('--category', help='Filter by category')
    
    # generate command
    gen_parser = subparsers.add_parser('generate', help='Generate workflow')
    gen_parser.add_argument('--name', required=True, help='Template name')
    gen_parser.add_argument('--output', help='Output file')
    gen_parser.add_argument('--format', choices=['json', 'yaml'], default='json')
    gen_parser.add_argument('--variables', help='JSON file with variables')
    
    args = parser.parse_args()
    
    manager = TemplateManager()
    
    if args.command == 'list':
        templates = manager.list_templates(
            category=getattr(args, 'category', None),
            platform=getattr(args, 'platform', None)
        )
        
        print(f"\nFound {len(templates)} templates:\n")
        for t in templates:
            print(f"  [{t['platform']}] {t['name']}")
            print(f"    {t['description']}")
            print()
    
    elif args.command == 'get':
        template = manager.get_template(args.name, args.platform)
        if not template:
            print(f"Template not found: {args.name}")
            sys.exit(1)
        
        output = json.dumps(template, indent=2)
        
        if args.output:
            Path(args.output).write_text(output)
            print(f"✓ Saved to {args.output}")
        else:
            print(output)
    
    elif args.command == 'search':
        results = manager.search_templates(
            keyword=args.keyword,
            platform=getattr(args, 'platform', None),
            category=getattr(args, 'category', None)
        )
        
        print(f"\nFound {len(results)} matching templates:\n")
        for r in results:
            print(f"  [{r['platform']}] {r['name']}")
            print(f"    {r['description']}")
    
    elif args.command == 'generate':
        variables = None
        if args.variables:
            variables = json.loads(Path(args.variables).read_text())
        
        workflow = manager.generate_workflow(
            name=args.name,
            variables=variables,
            output_format=args.format
        )
        
        if args.output:
            Path(args.output).write_text(workflow)
            print(f"✓ Generated workflow: {args.output}")
        else:
            print(workflow)
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()