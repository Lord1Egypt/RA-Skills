import xmlrpc.client
import os
import sys
import urllib.request
import urllib.parse
import re

def get_linkedin_url(query):
    url = 'https://html.duckduckgo.com/html/'
    data = urllib.parse.urlencode({'q': query}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
        # Search for linkedin.com/in/ links in the raw duckduckgo HTML
        match = re.search(r'href=[\'"]([^\'"]*linkedin\.com/in/[^\'"]*)[\'"]', html)
        if match:
            url_str = match.group(1)
            # Remove any URL encoding DuckDuckGo might have wrapped around it
            url_str = urllib.parse.unquote(url_str)
            if 'uddg=' in url_str:
                url_str = url_str.split('uddg=')[1].split('&')[0]
            return urllib.parse.unquote(url_str)
    except Exception as e:
        print(f"Search failed for {query}: {e}")
    return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 update_linkedin.py <partner_id>")
        sys.exit(1)
        
    partner_id = int(sys.argv[1])
    
    url = os.environ.get('ODOO_URL')
    db = os.environ.get('ODOO_DB')
    username = os.environ.get('ODOO_USERNAME')
    password = os.environ.get('ODOO_API_KEY') or os.environ.get('ODOO_PASSWORD')
    
    if not all([url, db, username, password]):
        print("Missing Odoo credentials in environment variables.")
        sys.exit(1)

    try:
        common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
        uid = common.authenticate(db, username, password, {})
        if not uid:
            print("Authentication failed.")
            sys.exit(1)
            
        models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
        
        # Read the partner
        partners = models.execute_kw(
            db, uid, password,
            'res.partner', 'read',
            [[partner_id]],
            {'fields': ['name', 'parent_id', 'x_linkedin_url']}
        )
        
        if not partners:
            print(f"Partner {partner_id} not found.")
            sys.exit(1)
            
        partner = partners[0]
        
        if partner.get('x_linkedin_url'):
            print(f"Partner already has a LinkedIn URL: {partner['x_linkedin_url']}")
            # Allow overwrite? Let's just update it anyway or skip? We'll proceed.
            
        name = partner.get('name', '')
        company_name = ''
        if partner.get('parent_id'):
            # parent_id is usually a list: [id, display_name]
            company_name = partner['parent_id'][1]
            
        search_query = f"site:linkedin.com/in {name} {company_name}".strip()
        print(f"Searching for: {search_query}")
        
        linkedin_url = get_linkedin_url(search_query)
        if linkedin_url:
            print(f"Found LinkedIn URL: {linkedin_url}")
            models.execute_kw(
                db, uid, password,
                'res.partner', 'write',
                [[partner_id], {'x_linkedin_url': linkedin_url}]
            )
            print("Successfully updated partner in Odoo.")
        else:
            print("Could not find a LinkedIn URL for this contact.")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()