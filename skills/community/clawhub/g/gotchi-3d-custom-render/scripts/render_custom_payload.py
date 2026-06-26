#!/usr/bin/env python3
import argparse
import json
import re

p = argparse.ArgumentParser()
p.add_argument('--haunt-id', type=int, default=1)
p.add_argument('--collateral', required=True)
p.add_argument('--eye-shape', required=True)
p.add_argument('--eye-color', required=True)
p.add_argument('--skin-id', type=int, default=0)
p.add_argument('--body', type=int, default=0)
p.add_argument('--face', type=int, default=0)
p.add_argument('--eyes', type=int, default=0)
p.add_argument('--head', type=int, default=0)
p.add_argument('--pet', type=int, default=0)
p.add_argument('--hand-left', type=int, default=0)
p.add_argument('--hand-right', type=int, default=0)
p.add_argument('--background', default='transparent')
p.add_argument('--pose', default='idle')
p.add_argument('--slug')
args = p.parse_args()
slug = args.slug or re.sub(r'[^a-z0-9]+', '-', f"{args.collateral}-{args.eye_shape}-{args.eye_color}-{args.head}-{args.body}-{args.face}".lower()).strip('-') or 'custom-gotchi'
out_base = f'/tmp/openclaw/custom-gotchi-{slug}'
payload = {
  'haunt_id': args.haunt_id,
  'collateral': args.collateral,
  'eye_shape': args.eye_shape,
  'eye_color': args.eye_color,
  'skin_id': args.skin_id,
  'wearables': {
    'body': args.body,
    'face': args.face,
    'eyes': args.eyes,
    'head': args.head,
    'pet': args.pet,
    'hand_left': args.hand_left,
    'hand_right': args.hand_right,
  },
  'background': args.background,
  'pose': args.pose,
  'output': {
    'slug': slug,
    'full_png': f'{out_base}-full.png',
    'headshot_png': f'{out_base}-headshot.png',
    'manifest_json': f'{out_base}-manifest.json',
  }
}
print(json.dumps(payload, indent=2))
