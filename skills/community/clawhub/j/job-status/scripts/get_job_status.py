#!/usr/bin/env python3
"""
Job Status Query Script
Queries HPC/AI computing job status by jobId
"""

import sys
import json
import requests
import argparse
from datetime import datetime
from typing import Dict, Any, Optional


class JobStatusFetcher:
    """Job status fetcher"""
    
    BASE_URL = "http://www.aicnic.cn/jobs/api/jobs/infos/hpcai28"
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'OpenClaw-JobStatus/1.0.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
    
    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """
        Get job status
        
        Args:
            job_id: Job ID
            
        Returns:
            Dictionary containing job status
        """
        # Build complete URL
        url = f"{self.BASE_URL}/{job_id}"
        
        try:
            # Send GET request
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            # Parse JSON response
            data = response.json()
            
            # Validate response structure
            if not isinstance(data, dict):
                return self._create_error_response(job_id, "Invalid API response format")
            
            # Check return code
            if data.get('code') != 0:
                error_msg = data.get('message', 'API returned error')
                return self._create_error_response(job_id, f"API error: {error_msg}")
            
            # Extract data
            job_data = data.get('data', {})
            if not job_data:
                return self._create_error_response(job_id, "API returned empty data")
            
            # Get job status
            job_state = job_data.get('jobState')
            if job_state is None:
                return self._create_error_response(job_id, "Job state field not found")
            
            # Build success response
            return {
                'success': True,
                'jobId': job_id,
                'status': job_state,
                'details': {
                    'jobState': job_state,
                    'jobId': job_data.get('jobId'),
                    'jobName': job_data.get('jobName'),
                    'id': job_data.get('id'),
                    'hpcId': job_data.get('hpcId'),
                    'userId': job_data.get('userId'),
                    'submitTime': job_data.get('submitTime'),
                    'startTime': job_data.get('startTime'),
                    'endTime': job_data.get('endTime'),
                    'runTime': job_data.get('runTime'),
                    'partitionName': job_data.get('partitionName'),
                    'numNodes': job_data.get('numNodes'),
                    'numCPUs': job_data.get('numCPUs'),
                    'mem': job_data.get('mem'),
                    'command': job_data.get('command'),
                    'workDir': job_data.get('workDir'),
                    'exitCode': job_data.get('exitCode'),
                    'exitStatus': job_data.get('exitStatus')
                },
                'message': self._get_status_message(job_state),
                'timestamp': datetime.now().isoformat()
            }
            
        except requests.exceptions.Timeout:
            return self._create_error_response(job_id, "Request timeout")
        except requests.exceptions.ConnectionError:
            return self._create_error_response(job_id, "Network connection failed")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return self._create_error_response(job_id, "Job not found")
            else:
                return self._create_error_response(job_id, f"HTTP error: {e.response.status_code}")
        except json.JSONDecodeError:
            return self._create_error_response(job_id, "JSON parsing failed")
        except Exception as e:
            return self._create_error_response(job_id, f"Unknown error: {str(e)}")
    
    def _create_error_response(self, job_id: str, error_message: str) -> Dict[str, Any]:
        """Create error response"""
        return {
            'success': False,
            'jobId': job_id,
            'error': error_message,
            'message': f"Job {job_id} query failed: {error_message}",
            'timestamp': datetime.now().isoformat()
        }
    
    def _get_status_message(self, job_state: str) -> str:
        """Return friendly message based on status"""
        status_messages = {
            'PENDING': 'Job is queued and waiting',
            'RUNNING': 'Job is currently running',
            'COMPLETED': 'Job completed successfully',
            'FAILED': 'Job execution failed',
            'CANCELLED': 'Job was cancelled',
            'TIMEOUT': 'Job execution timed out',
            'SUSPENDED': 'Job is suspended',
            'CONFIGURING': 'Job is being configured'
        }
        
        return status_messages.get(job_state, f'Job status: {job_state}')


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Query HPC/AI computing job status')
    parser.add_argument('--job-id', '-j', required=True, help='Job ID')
    parser.add_argument('--timeout', '-t', type=int, default=30, help='Request timeout in seconds')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output mode')
    
    args = parser.parse_args()
    
    # Create fetcher instance
    fetcher = JobStatusFetcher(timeout=args.timeout)
    
    # Get job status
    result = fetcher.get_job_status(args.job_id)
    
    # Output result
    if args.verbose:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        # Concise output
        if result['success']:
            print(f"Job {result['jobId']} Status: {result['status']}")
            print(f"Details: {result['message']}")
            if result['details'].get('endTime'):
                print(f"End Time: {result['details']['endTime']}")
        else:
            print(f"Error: {result['error']}")
    
    # Return exit code
    sys.exit(0 if result['success'] else 1)


if __name__ == '__main__':
    main()