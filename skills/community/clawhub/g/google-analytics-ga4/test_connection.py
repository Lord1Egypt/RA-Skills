#!/usr/bin/env python3
"""
Verify Google Analytics credentials and Data API access.
"""

import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

try:
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import MetadataRequest
except ImportError:
    print("Missing dependency: google-analytics-data")
    print("  pip install google-analytics-data")
    sys.exit(1)


def check_credentials():
    print("Checking credentials...\n")

    env_creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if env_creds:
        print("GOOGLE_APPLICATION_CREDENTIALS is set")
        print(f"  Path: {env_creds}")
        if os.path.exists(env_creds):
            print("  File exists: yes")
        else:
            print("  File exists: NO")
            return False
    else:
        print("GOOGLE_APPLICATION_CREDENTIALS is not set")

    local_creds = os.path.join(SCRIPT_DIR, "ga-credentials.json")
    if os.path.exists(local_creds):
        print(f"Local key found: {local_creds}")
    else:
        print(f"No local ga-credentials.json at {local_creds}")

    if not env_creds and not os.path.exists(local_creds):
        print("\nNo credentials found.")
        print("1. Create a service account in Google Cloud")
        print("2. Download the JSON key")
        print("3. Save as ga-credentials.json here or set GOOGLE_APPLICATION_CREDENTIALS")
        print("\nSee SKILL.md for step-by-step setup.")
        return False

    return True


def check_api_access(property_id: str = None):
    print("\nChecking API access...\n")

    try:
        client = BetaAnalyticsDataClient()
        print("Client created successfully")
    except Exception as e:
        print(f"Failed to create client: {e}")
        print("\nCommon causes:")
        print("1. Invalid or corrupted JSON key")
        print("2. Wrong file permissions")
        print("3. Network issues")
        return False

    if not property_id:
        print("\nNo --property-id passed; skipping live property tests.")
        print("Run: python test_connection.py --property-id YOUR-PROPERTY-ID")
        return True

    print(f"\nProbing property: properties/{property_id}")

    try:
        print("Fetching metadata...")
        request = MetadataRequest(property=f"properties/{property_id}")
        response = client.get_metadata(request)

        dim_count = len(response.dimensions)
        metric_count = len(response.metrics)

        print("Metadata OK")
        print(f"  Dimensions: {dim_count}")
        print(f"  Metrics: {metric_count}")

        print("\nTrying realtime activeUsers...")
        from google.analytics.data_v1beta.types import (
            RunRealtimeReportRequest,
            Metric,
        )

        realtime_request = RunRealtimeReportRequest(
            property=f"properties/{property_id}",
            metrics=[Metric(name="activeUsers")],
        )
        realtime_response = client.run_realtime_report(realtime_request)

        active_users = 0
        if realtime_response.rows:
            active_users = realtime_response.rows[0].metric_values[0].value

        print("Realtime query OK")
        print(f"  activeUsers (sample): {active_users}")

        return True

    except Exception as e:
        error_msg = str(e)
        print(f"API call failed: {error_msg}")

        if "Permission denied" in error_msg:
            print("\nLikely cause: insufficient GA4 access")
            print("Fix:")
            print("1. Open the GA4 property")
            print("2. Admin > Property access management")
            print("3. Add the service account email (field client_email in the JSON) as Viewer")

        elif "has not been used" in error_msg:
            print("\nLikely cause: Data API not enabled")
            print("Fix: Google Cloud > APIs & Services > enable Google Analytics Data API")

        elif "invalid_property_id" in error_msg.lower():
            print("\nLikely cause: wrong property id")
            print("Fix: use the numeric GA4 property ID from Admin > Property settings")

        return False


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Google Analytics connectivity test")
    parser.add_argument(
        "--property-id",
        help="Numeric GA4 property ID (optional but recommended)",
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Google Analytics connectivity test")
    print("=" * 60)

    if not check_credentials():
        sys.exit(1)

    if not check_api_access(args.property_id):
        sys.exit(1)

    print("\n" + "=" * 60)
    print("All checks passed")
    print("=" * 60)
    print("\nNext:")
    print(f"  python ga_query.py --action realtime --property-id {args.property_id or 'YOUR-PROPERTY-ID'}")


if __name__ == "__main__":
    main()
