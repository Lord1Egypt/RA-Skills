#!/usr/bin/env python3
"""Notify Tool - Send notifications."""

import argparse
import os
import sys


def send_desktop_notification(title: str, message: str, urgency: str = 'normal'):
    """Send desktop notification."""
    try:
        # Try notify-send (Linux)
        urgency_map = {'low': 'low', 'normal': 'normal', 'critical': 'critical'}
        os.system(f'notify-send -u {urgency_map.get(urgency, "normal")} "{title}" "{message}"')
    except:
        print(f"[NOTIFICATION] {title}: {message}")


def main():
    parser = argparse.ArgumentParser(description='Send notifications')
    parser.add_argument('message', help='Notification message')
    parser.add_argument('--title', default='Notification', help='Title')
    parser.add_argument('--urgency', default='normal', choices=['low', 'normal', 'critical'])
    
    args = parser.parse_args()
    send_desktop_notification(args.title, args.message, args.urgency)


if __name__ == '__main__':
    main()
