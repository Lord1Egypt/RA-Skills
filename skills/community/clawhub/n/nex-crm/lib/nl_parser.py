"""
Nex CRM - Natural Language Parser
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)

Parse natural language inputs for prospect creation and activity logging.
"""
import re
from datetime import datetime, timedelta


def parse_prospect_input(text):
    """
    Parse natural language input for prospect creation.
    Examples:
    - "nieuwe lead Bakkerij Peeters, Gent, website nodig"
    - "ECHO Management, Jan contact, jan@echo.be, +32 471 123456"
    """
    data = {}

    # Try to extract company name (usually first meaningful phrase)
    # Common patterns: "Company Name," or "Company Name -" or start of sentence
    company_match = re.search(r'^(?:nieuwe\s+lead\s+)?([A-Z][A-Za-z\s&\'.-]+?)(?:\s*,|\s*-|$)', text, re.IGNORECASE)
    if company_match:
        data['company'] = company_match.group(1).strip()

    # Extract contact name (after "contact" or standalone names)
    contact_match = re.search(r'(?:contact[:\s]+)?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', text)
    if contact_match and contact_match.group(1) != data.get('company', ''):
        data['contact_name'] = contact_match.group(1).strip()

    # Extract email
    email_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', text)
    if email_match:
        data['email'] = email_match.group(1)

    # Extract phone (various formats)
    phone_match = re.search(r'(?:\+|0)?(?:32\s?)?[\s\d\-().]{8,}', text)
    if phone_match:
        data['phone'] = phone_match.group(0).strip()

    # Extract priority (hot, warm, cold)
    priority_match = re.search(r'\b(hot|warm|cold)\b', text, re.IGNORECASE)
    if priority_match:
        data['priority'] = priority_match.group(1).lower()

    # Extract value (EUR amounts)
    value_match = re.search(r'€?\s*(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:eur|euro|/mo|/month)?', text, re.IGNORECASE)
    if value_match:
        value_str = value_match.group(1).replace(',', '')
        try:
            data['value'] = int(float(value_str))
        except ValueError:
            pass

    # Extract source (scrape, referral, inbound, outreach, event, website)
    source_match = re.search(r'\b(scrape|scraping|referral|inbound|outreach|event|website)\b', text, re.IGNORECASE)
    if source_match:
        source_str = source_match.group(1).lower()
        if source_str.startswith('scrap'):
            data['source'] = 'scrape'
        else:
            data['source'] = source_str

    # Extract location
    location_match = re.search(r'(?:in\s+|,\s*)([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', text)
    if location_match:
        data['location'] = location_match.group(1).strip()

    # Extract needs/notes
    needs_match = re.search(r'(?:needs?|wants?|looking for)\s+([^,.]*)', text, re.IGNORECASE)
    if needs_match:
        data['notes'] = needs_match.group(1).strip()

    return data


def parse_activity_input(text):
    """
    Parse natural language for activity logging.
    Returns: (activity_data, prospect_name)

    Examples:
    - "had a call with Jan from ECHO Management, interested in premium package"
    - "Jan confirmed demo for Thursday 2pm"
    """
    activity_data = {}
    prospect_name = None

    # Extract company/prospect name (usually after "from", "with", or capitalized phrase)
    company_match = re.search(r'(?:from|with|for)\s+(?:[A-Z][a-z]+\s+)?([A-Z][A-Za-z\s&\'.-]+)', text)
    if company_match:
        prospect_name = company_match.group(1).strip()

    # Determine activity type from keywords
    if re.search(r'\b(call|phone|spoke|talked|discussed)\b', text, re.IGNORECASE):
        activity_data['type'] = 'call'
    elif re.search(r'\b(email|sent|message|replied)\b', text, re.IGNORECASE):
        activity_data['type'] = 'email'
    elif re.search(r'\b(meeting|met)\b', text, re.IGNORECASE):
        activity_data['type'] = 'meeting'
    elif re.search(r'\b(demo|showed|presentation)\b', text, re.IGNORECASE):
        activity_data['type'] = 'demo'
    elif re.search(r'\b(proposal|quote|offer)\b', text, re.IGNORECASE):
        activity_data['type'] = 'proposal'
    else:
        activity_data['type'] = 'note'

    # Extract summary
    activity_data['summary'] = text.strip()

    # Extract channel if mentioned
    if re.search(r'\b(telegram|whatsapp|slack)\b', text, re.IGNORECASE):
        match = re.search(r'\b(telegram|whatsapp|slack)\b', text, re.IGNORECASE)
        activity_data['channel'] = match.group(1).lower()

    # Extract direction
    if re.search(r'\b(received|got|inbound|incoming)\b', text, re.IGNORECASE):
        activity_data['direction'] = 'inbound'
    else:
        activity_data['direction'] = 'outbound'

    return activity_data, prospect_name


def parse_date_input(date_str):
    """
    Parse date strings like:
    - "2026-04-10"
    - "tomorrow"
    - "in 3d" (3 days)
    - "next Monday"
    """
    date_str = date_str.lower().strip()

    # ISO format
    try:
        return datetime.fromisoformat(date_str).isoformat()
    except ValueError:
        pass

    # Relative dates
    now = datetime.now()

    if date_str == 'tomorrow':
        return (now + timedelta(days=1)).isoformat()

    if date_str == 'today':
        return now.isoformat()

    # "in Xd" or "in Xdays"
    match = re.match(r'in\s+(\d+)\s*(?:d|days)?', date_str)
    if match:
        days = int(match.group(1))
        return (now + timedelta(days=days)).isoformat()

    # "in X hours"
    match = re.match(r'in\s+(\d+)\s*(?:h|hours)?', date_str)
    if match:
        hours = int(match.group(1))
        return (now + timedelta(hours=hours)).isoformat()

    # Default to ISO if parseable, otherwise return as-is
    return date_str
