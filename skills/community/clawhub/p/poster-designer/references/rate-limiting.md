# Rate Limiting Configuration

## User Rate Limits
- Max 5 requests per minute per user
- Max 50 requests per hour per user
- Queue max 3 concurrent jobs per user

## Global Rate Limits
- Max 20 concurrent image generations
- Queue overflow: Wait or reject with message

## Implementation
Use a simple queue system:
- Store pending jobs in memory or Redis
- Process FIFO
- Notify user of queue position

## User Tiers
- Free tier: 10 images/day
- Standard tier: 100 images/day  
- Pro tier: Unlimited

## Priority System
- Owner/Admin: Priority 1 (immediate)
- Manager: Priority 2 (fast queue)
- User: Priority 3 (standard queue)
