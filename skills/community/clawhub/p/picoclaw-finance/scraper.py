"""
LinkedIn Jobs Scraper - Public API Endpoint

This module scrapes LinkedIn job postings using the public, unauthenticated endpoint.
No login required. Works on VPS without browser.
"""

import requests
from bs4 import BeautifulSoup
import time
import random
import json
import csv
from typing import Dict, List, Optional, Any
from urllib.parse import urlencode
import re


class LinkedInJobsScraper:
    """Scraper for LinkedIn job postings using public API endpoints."""
    
    BASE_URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
    JOB_DETAILS_URL = "https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
    
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    ]
    
    def __init__(self, delay_range: tuple = (2, 5), max_retries: int = 3):
        """
        Initialize the scraper.
        
        Args:
            delay_range: Min and max delay between requests in seconds
            max_retries: Maximum number of retries for failed requests
        """
        self.delay_range = delay_range
        self.max_retries = max_retries
        self.session = requests.Session()
        self._update_user_agent()
    
    def _update_user_agent(self):
        """Randomly select a user agent."""
        self.session.headers.update({
            "User-Agent": random.choice(self.USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Cache-Control": "max-age=0",
        })
    
    def _build_search_params(self, keywords: str, location: str, 
                            remote: Optional[str] = None,
                            experience: Optional[str] = None,
                            job_type: Optional[str] = None,
                            posted: Optional[str] = None,
                            salary_min: Optional[int] = None,
                            company: Optional[str] = None,
                            industry: Optional[str] = None,
                            sort: Optional[str] = None,
                            start: int = 0) -> Dict[str, Any]:
        """Build search parameters for LinkedIn Jobs API."""
        
        params = {
            "keywords": keywords.replace(" ", "+"),
            "location": location.replace(" ", "+"),
            "original_referer": "",
            "start": start,
        }
        
        # Remote filter
        if remote == "only":
            params["f_WT"] = 2  # Remote only
        elif remote == "yes":
            params["f_WT"] = "2,3"  # Remote or Hybrid
        elif remote == "no":
            params["f_WT"] = 1  # On-site only
        
        # Experience level
        experience_map = {
            "internship": "1",
            "entry": "2",
            "associate": "3",
            "mid-senior": "4",
            "director": "5",
            "executive": "6",
        }
        if experience and experience in experience_map:
            params["f_E"] = experience_map[experience]
        
        # Job type
        job_type_map = {
            "full-time": "F",
            "part-time": "P",
            "contract": "C",
            "temporary": "T",
            "internship": "I",
        }
        if job_type and job_type in job_type_map:
            params["f_JT"] = job_type_map[job_type]
        
        # Posted date
        posted_map = {
            "last-24h": "r86400",
            "last-week": "r604800",
            "last-month": "r2592000",
            "anytime": "",
        }
        if posted and posted in posted_map and posted_map[posted]:
            params["f_TPR"] = posted_map[posted]
        
        # Salary filter (min salary in USD)
        if salary_min:
            params["f_SALARY"] = str(salary_min)
        
        # Company filter (LinkedIn company ID)
        if company:
            params["f_C"] = company
        
        # Industry filter (LinkedIn industry ID)
        if industry:
            params["f_I"] = industry
        
        # Sort order
        if sort == "date":
            params["sortBy"] = "DD"  # Most recent
        elif sort == "relevance":
            params["sortBy"] = "R"   # Most relevant
        
        return params
    
    def _delay(self):
        """Add random delay between requests."""
        delay = random.uniform(*self.delay_range)
        time.sleep(delay)
    
    def search_jobs(self, keywords: str, location: str,
                   remote: Optional[str] = None,
                   experience: Optional[str] = None,
                   job_type: Optional[str] = None,
                   posted: Optional[str] = None,
                   salary_min: Optional[int] = None,
                   company: Optional[str] = None,
                   industry: Optional[str] = None,
                   sort: Optional[str] = None,
                   limit: int = 25) -> List[Dict[str, Any]]:
        """
        Search for LinkedIn job postings.
        
        Args:
            keywords: Job title or skills to search for
            location: Geographic location
            remote: "only" (remote only), "yes" (remote/hybrid), "no" (on-site only)
            experience: Experience level filter
            job_type: Employment type filter
            posted: When the job was posted
            salary_min: Minimum salary in USD
            company: LinkedIn company ID to filter by
            industry: LinkedIn industry ID to filter by
            sort: "date" or "relevance"
            limit: Maximum number of jobs to return (default: 25)
            
        Returns:
            List of job dictionaries
        """
        jobs = []
        start = 0
        max_results_per_page = 25
        
        while len(jobs) < limit:
            params = self._build_search_params(
                keywords=keywords,
                location=location,
                remote=remote,
                experience=experience,
                job_type=job_type,
                posted=posted,
                salary_min=salary_min,
                company=company,
                industry=industry,
                sort=sort,
                start=start
            )
            
            try:
                response = self.session.get(
                    self.BASE_URL,
                    params=params,
                    timeout=30,
                    allow_redirects=True
                )
                
                if response.status_code == 429:
                    print(f"Rate limited. Waiting 30 seconds...")
                    time.sleep(30)
                    continue
                elif response.status_code != 200:
                    print(f"Error: Status code {response.status_code}")
                    break
                
                parsed_jobs = self._parse_search_results(response.text)
                
                if not parsed_jobs:
                    print("No more jobs found or authentication wall reached.")
                    break
                
                jobs.extend(parsed_jobs)
                
                if len(parsed_jobs) < max_results_per_page:
                    break
                
                start += max_results_per_page
                self._delay()
                
            except requests.RequestException as e:
                print(f"Request error: {e}")
                break
        
        return jobs[:limit]
    
    def _parse_search_results(self, html: str) -> List[Dict[str, Any]]:
        """Parse job search results from HTML."""
        soup = BeautifulSoup(html, 'html.parser')
        jobs = []
        
        job_cards = soup.find_all('div', class_='base-search-card')
        
        for card in job_cards:
            try:
                # Job title
                title_elem = card.find('h3', class_='base-search-card__title')
                title = title_elem.get_text(strip=True) if title_elem else None
                
                # Company
                company_elem = card.find('h4', class_='base-search-card__subtitle')
                company = company_elem.get_text(strip=True) if company_elem else None
                
                # Location
                location_elem = card.find('span', class_='job-search-card__location')
                location = location_elem.get_text(strip=True) if location_elem else None
                
                # URL
                link_elem = card.find('a', class_='base-card__full-link')
                url = link_elem.get('href') if link_elem else None
                
                # Extract job ID from URL
                job_id = self._extract_job_id(url)
                
                if title and company and url:
                    jobs.append({
                        "title": title,
                        "company": company,
                        "location": location,
                        "url": url,
                        "job_id": job_id,
                        "posted_date": None,
                        "description": None,
                        "employment_type": None,
                        "seniority_level": None,
                        "job_function": None,
                        "industries": None,
                    })
            except Exception as e:
                continue
        
        return jobs
    
    def _extract_job_id(self, url: Optional[str]) -> Optional[str]:
        """Extract job ID from LinkedIn job URL."""
        if not url:
            return None
        
        # Pattern: extract ID from end of URL path (e.g., .../fullstack-4315351945?...)
        match = re.search(r'-(\d+)(?:[?&]|$)', url)
        if match:
            return match.group(1)
        
        # Pattern: /jobs/view/1234567890
        match = re.search(r'/jobs/view/(\d+)', url)
        if match:
            return match.group(1)
        
        # If URL is just the ID
        if url.isdigit():
            return url
        
        return None
    
    def get_job_details(self, job_id: str) -> Optional[Dict[str, Any]]:
        """
        Get full details for a specific job posting.
        
        Args:
            job_id: The numeric job ID
            
        Returns:
            Job details dictionary or None if not found
        """
        try:
            url = self.JOB_DETAILS_URL.format(job_id=job_id)
            
            response = self.session.get(url, timeout=30, allow_redirects=True)
            
            if response.status_code != 200:
                return None
            
            return self._parse_job_details(response.text, job_id)
            
        except requests.RequestException as e:
            print(f"Error fetching job details: {e}")
            return None
    
    def _parse_job_details(self, html: str, job_id: str) -> Optional[Dict[str, Any]]:
        """Parse detailed job information from HTML."""
        soup = BeautifulSoup(html, 'html.parser')
        
        try:
            # Title
            title_elem = soup.select_one('.top-card-layout__title')
            title = title_elem.get_text(strip=True) if title_elem else None
            
            # Company
            company_elem = soup.select_one('a.topcard__org-name-link')
            company = company_elem.get_text(strip=True) if company_elem else None
            
            # Location
            location_elem = soup.select_one('span.topcard__flavor--bullet')
            location = location_elem.get_text(strip=True) if location_elem else None
            
            # Posted time
            posted_elem = soup.select_one('span.posted-time-ago__text')
            posted_date = posted_elem.get_text(strip=True) if posted_elem else None
            
            # Description
            desc_elem = soup.select_one('div.show-more-less-html__markup')
            description = desc_elem.get_text(strip=True) if desc_elem else None
            
            # Job details (seniority, type, function, industries)
            details_list = soup.select('ul.job-details-jobs-unified-top-card__primary-details li')
            
            employment_type = None
            seniority_level = None
            job_function = None
            industries = None
            
            for detail in details_list:
                text = detail.get_text(strip=True)
                if any(kw in text for kw in ('Emprego', 'Tipo', 'Full-time', 'Part-time', 'Contract', 'Temporary', 'Internship', 'Employment')):
                    employment_type = text
                elif any(kw in text for kw in ('Nível', 'Seniority', 'Mid-Senior', 'Entry', 'Director', 'Executive', 'Associate')):
                    seniority_level = text
                elif any(kw in text for kw in ('Função', 'Function', 'Engineering', 'Software')):
                    job_function = text
                elif any(kw in text for kw in ('Setores', 'Industries', 'Software Development')):
                    industries = text
            
            return {
                "job_id": job_id,
                "title": title,
                "company": company,
                "location": location,
                "posted_date": posted_date,
                "description": description,
                "employment_type": employment_type,
                "seniority_level": seniority_level,
                "job_function": job_function,
                "industries": industries,
                "url": f"https://www.linkedin.com/jobs/view/{job_id}",
            }
            
        except Exception as e:
            print(f"Error parsing job details: {e}")
            return None
    
    def save_to_csv(self, jobs: List[Dict[str, Any]], filename: str):
        """Save jobs to CSV file."""
        if not jobs:
            print("No jobs to save.")
            return
        
        fieldnames = jobs[0].keys()
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(jobs)
        
        print(f"Saved {len(jobs)} jobs to {filename}")
    
    def save_to_json(self, jobs: List[Dict[str, Any]], filename: str):
        """Save jobs to JSON file."""
        if not jobs:
            print("No jobs to save.")
            return
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(jobs, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(jobs)} jobs to {filename}")
    
    def search_and_save(self, keywords: str, location: str,
                       output: str, limit: int = 25,
                       remote: Optional[str] = None,
                       experience: Optional[str] = None,
                       job_type: Optional[str] = None,
                       posted: Optional[str] = None,
                       salary_min: Optional[int] = None,
                       company: Optional[str] = None,
                       industry: Optional[str] = None,
                       sort: Optional[str] = None):
        """
        Search for jobs and save to file.
        
        Args:
            keywords: Job search keywords
            location: Job location
            output: Output filename (CSV or JSON)
            limit: Maximum number of jobs
            remote: Remote work filter
            experience: Experience level filter
            job_type: Employment type filter
            posted: Posted date filter
            salary_min: Minimum salary in USD
            company: LinkedIn company ID
            industry: LinkedIn industry ID
            sort: "date" or "relevance"
        """
        jobs = self.search_jobs(
            keywords=keywords,
            location=location,
            limit=limit,
            remote=remote,
            experience=experience,
            job_type=job_type,
            posted=posted,
            salary_min=salary_min,
            company=company,
            industry=industry,
            sort=sort
        )
        
        if output.endswith('.csv'):
            self.save_to_csv(jobs, output)
        elif output.endswith('.json'):
            self.save_to_json(jobs, output)
        else:
            # Default to CSV
            self.save_to_csv(jobs, output + '.csv')
        
        return jobs


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='LinkedIn Jobs Scraper')
    parser.add_argument('--keywords', required=True, help='Job search keywords')
    parser.add_argument('--location', required=True, help='Job location')
    parser.add_argument('--remote', choices=['only', 'yes', 'no'], help='Remote work filter')
    parser.add_argument('--experience', choices=['internship', 'entry', 'associate', 'mid-senior', 'director', 'executive'], help='Experience level')
    parser.add_argument('--job-type', choices=['full-time', 'part-time', 'contract', 'temporary', 'internship'], help='Job type')
    parser.add_argument('--posted', choices=['last-24h', 'last-week', 'last-month', 'anytime'], help='Posted date filter')
    parser.add_argument('--salary-min', type=int, help='Minimum salary in USD')
    parser.add_argument('--company', help='LinkedIn company ID to filter by')
    parser.add_argument('--industry', help='LinkedIn industry ID to filter by')
    parser.add_argument('--sort', choices=['date', 'relevance'], help='Sort order')
    parser.add_argument('--limit', type=int, default=25, help='Maximum number of jobs')
    parser.add_argument('--output', help='Output file (CSV or JSON)')
    
    args = parser.parse_args()
    
    scraper = LinkedInJobsScraper()
    
    print(f"Searching for '{args.keywords}' in {args.location}...")
    
    jobs = scraper.search_jobs(
        keywords=args.keywords,
        location=args.location,
        remote=args.remote,
        experience=args.experience,
        job_type=args.job_type,
        posted=args.posted,
        salary_min=args.salary_min,
        company=args.company,
        industry=args.industry,
        sort=args.sort,
        limit=args.limit
    )
    
    print(f"\nFound {len(jobs)} jobs:\n")
    
    for i, job in enumerate(jobs, 1):
        print(f"{i}. {job['title']} at {job['company']}")
        print(f"   Location: {job['location']}")
        print(f"   URL: {job['url']}")
        print()
    
    if args.output:
        scraper.search_and_save(
            keywords=args.keywords,
            location=args.location,
            output=args.output,
            limit=args.limit,
            remote=args.remote,
            experience=args.experience,
            job_type=args.job_type,
            posted=args.posted,
            salary_min=args.salary_min,
            company=args.company,
            industry=args.industry,
            sort=args.sort
        )


if __name__ == '__main__':
    main()