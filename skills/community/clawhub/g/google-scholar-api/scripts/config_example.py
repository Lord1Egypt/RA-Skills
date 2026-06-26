"""
Configuration example for Google Scholar API skill.

This file shows how to set up and use the Google Scholar search functionality.
"""

import os
from google_scholar_search import GoogleScholarSearch

# Set your SerpAPI key (get one from https://serpapi.com/)
os.environ['SERP_API_KEY'] = 'your_serpapi_key_here'

# Or pass it directly when creating the client
# client = GoogleScholarSearch(api_key='your_serpapi_key_here')

def example_basic_search():
    """Example of basic search functionality."""
    client = GoogleScholarSearch()
    
    # Search for papers
    query = "machine learning deep neural networks"
    results = client.search(query, num_results=5)
    
    # Parse results
    papers = client.parse_results(results)
    
    print(f"Found {len(papers)} papers for query: '{query}'")
    print(f"Total results: {results.get('search_information', {}).get('total_results', 'N/A')}")
    
    for i, paper in enumerate(papers):
        print(f"\n{i+1}. {paper['title']}")
        
        # Display authors
        if paper['authors']:
            author_names = [author.get('name', '') for author in paper['authors'][:3]]
            print(f"   Authors: {', '.join(author_names)}")
            if len(paper['authors']) > 3:
                print(f"   ... and {len(paper['authors']) - 3} more")
        
        print(f"   Year: {paper['year']}")
        print(f"   Citations: {paper['cited_by']}")
        
        if paper.get('has_pdf'):
            print(f"   PDF: ✅ Available")
            if 'pdf_link' in paper:
                print(f"   Link: {paper['pdf_link'][:80]}...")
        else:
            print(f"   PDF: ❌ Not available")
        
        # Show result ID for advanced searches
        if paper.get('result_id'):
            print(f"   Result ID: {paper['result_id']}")
        if paper.get('cites_id'):
            print(f"   Cites ID: {paper['cites_id']}")
        if paper.get('cluster_id'):
            print(f"   Cluster ID: {paper['cluster_id']}")

def example_download_pdfs():
    """Example of searching and downloading PDFs."""
    client = GoogleScholarSearch()
    
    # Search and download
    query = "transformer architecture attention mechanism"
    result = client.search_and_download(
        query=query,
        download_dir="./scholar_papers",
        max_papers=3
    )
    
    print(f"\nSearch completed for: {query}")
    print(f"Downloaded {result['successful_downloads']} out of {result['total_results']} papers")

def example_author_search():
    """Example of searching by author."""
    client = GoogleScholarSearch()
    
    # Search papers by specific author
    print("Searching papers by Yoshua Bengio:")
    results = client.search_by_author("Yoshua Bengio", num_results=5)
    papers = client.parse_results(results)
    
    for i, paper in enumerate(papers):
        print(f"{i+1}. {paper['title'][:80]}... ({paper['year']})")

def example_citation_search():
    """Example of searching citations."""
    client = GoogleScholarSearch()
    
    # You need a real cites_id from a previous search
    # This is just an example format
    example_cites_id = "9943926152122871332"  # Example ID
    
    print(f"Searching papers citing article {example_cites_id}:")
    results = client.search_cited_by(example_cites_id, num_results=5)
    
    if "organic_results" in results:
        papers = client.parse_results(results)
        for i, paper in enumerate(papers[:3]):
            print(f"{i+1}. {paper['title'][:80]}...")

def example_advanced_filters():
    """Example with advanced search filters."""
    client = GoogleScholarSearch()
    
    # Search with multiple filters
    query = "transformer architecture attention"
    results = client.search(
        query=query,
        num_results=8,
        year_from=2022,
        sort_by="date",  # Sort by most recent
        include_citations=True,
        language="en",
        only_reviews=False
    )
    
    papers = client.parse_results(results)
    
    search_info = results.get('search_information', {})
    print(f"Search: {query}")
    print(f"Total results: {search_info.get('total_results', 'N/A')}")
    print(f"Recent papers (since 2022):")
    
    for paper in papers:
        authors = [author.get('name', '') for author in paper['authors'][:2]]
        author_str = ', '.join(authors) + (' et al.' if len(paper['authors']) > 2 else '')
        
        print(f"  • {paper['title'][:70]}...")
        print(f"    {author_str} ({paper['year']}) - {paper['cited_by']} citations")
        if paper.get('has_pdf'):
            print(f"    📄 PDF available")

def example_command_line_usage():
    """Example of command-line usage."""
    print("Command-line examples:")
    print("=" * 50)
    
    examples = [
        ("Basic search", 'python google_scholar_search.py "machine learning" --num 10'),
        ("Author search", 'python google_scholar_search.py \'author:"Andrew Ng"\' --num 5'),
        ("Year filter", 'python google_scholar_search.py "deep learning" --year-from 2020 --year-to 2023'),
        ("Sort by date", 'python google_scholar_search.py "transformer" --sort date'),
        ("No citations", 'python google_scholar_search.py "reinforcement learning" --no-citations'),
        ("Search only", 'python google_scholar_search.py "computer vision" --no-download'),
        ("JSON output", 'python google_scholar_search.py "natural language processing" --json-only'),
    ]
    
    for desc, cmd in examples:
        print(f"\n{desc}:")
        print(f"  {cmd}")

if __name__ == "__main__":
    print("Google Scholar API Examples - SerpAPI Integration")
    print("=" * 60)
    
    print("\nAvailable examples:")
    print("1. example_basic_search() - Basic search functionality")
    print("2. example_download_pdfs() - Search and download PDFs")
    print("3. example_author_search() - Search by author")
    print("4. example_citation_search() - Search citations")
    print("5. example_advanced_filters() - Advanced search filters")
    print("6. example_command_line_usage() - Command-line examples")
    
    print("\n" + "=" * 60)
    print("Important Notes:")
    print("- Replace 'your_serpapi_key_here' with your actual SerpAPI key")
    print("- Get a free API key from: https://serpapi.com/")
    print("- Free plan: 250 searches/month, 50 searches/hour")
    print("- API documentation: https://serpapi.com/google-scholar-api")
    print("- Playground: https://serpapi.com/playground?engine=google_scholar")
    
    print("\nTo run an example, uncomment it in the code.")
    print("Example: Uncomment 'example_basic_search()' and run the script.")