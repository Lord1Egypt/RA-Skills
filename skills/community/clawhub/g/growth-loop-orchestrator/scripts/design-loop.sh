#!/bin/bash
#
# design-loop.sh - Design a growth loop for a skill
# Usage: ./design-loop.sh --type <viral|content|network|engagement> --skill <name>
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="${GROWTH_DATA_DIR:-$SKILL_DIR/data}"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Parse arguments
LOOP_TYPE=""
SKILL_NAME=""
OUTPUT_FILE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --type)
            LOOP_TYPE="$2"
            shift 2
            ;;
        --skill)
            SKILL_NAME="$2"
            shift 2
            ;;
        --output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

if [[ -z "$LOOP_TYPE" || -z "$SKILL_NAME" ]]; then
    echo "Usage: $0 --type <viral|content|network|engagement> --skill <name> [--output file.md]"
    exit 1
fi

# Validate loop type
if [[ ! "$LOOP_TYPE" =~ ^(viral|content|network|engagement|feedback)$ ]]; then
    echo "Error: Loop type must be one of: viral, content, network, engagement, feedback"
    exit 1
fi

# Create data directory
mkdir -p "$DATA_DIR"

DESIGN_FILE="${OUTPUT_FILE:-$DATA_DIR/LOOP-DESIGN-${SKILL_NAME}-$(date +%Y%m%d).md}"

echo -e "${BLUE}🔄 Designing $LOOP_TYPE growth loop for: $SKILL_NAME${NC}"
echo "================================"

# Generate loop design based on type
case $LOOP_TYPE in
    viral)
        cat > "$DESIGN_FILE" << EOF
# Growth Loop Design: Viral Loop for ${SKILL_NAME}

**Type**: Viral  
**Skill**: ${SKILL_NAME}  
**Designed**: $(date -u +%Y-%m-%dT%H:%M:%SZ)

## Loop Diagram

\`\`\`
[New User] → [Use ${SKILL_NAME}] → [Create Output] → [Share Output]
    ↑                                                    ↓
    └──────────── [View Output] ← [Try Skill] ←── [New User Sees]
\`\`\`

## Components

### Input: User Creates Content
- **Source**: User uses ${SKILL_NAME}
- **Volume**: ~50 outputs/day (projected)
- **Quality**: High (user-generated, contextual)

### Action: User Shares
- **Trigger**: Completion of skill task
- **Channels**: Social media, email, direct link
- **Friction**: Medium (requires user action)

### Output: Sharable Result
- **Format**: Image, document, or interactive result
- **Value**: Demonstrates skill capability
- **Branding**: Subtle skill attribution

### Conversion: View → Try
- **Mechanism**: "Try it yourself" CTA on shared content
- **Landing**: Skill entry point with context
- **Target Rate**: 25%

### Amplification
- **Social Proof**: "X people used this"
- **Incentive**: Free credits for referrals
- **Network**: See friends' activity

## Metrics

| Metric | Target |
|--------|--------|
| Share Rate | 40% |
| View-to-Try Rate | 25% |
| Try-to-Complete Rate | 60% |
| Viral Coefficient (K) | 0.5 |
| Cycle Time | 24 hours |

## Implementation Plan

### Phase 1: Foundation (Week 1)
- [ ] Add share button to outputs
- [ ] Create shareable formats
- [ ] Build landing page for shared content
- [ ] Add attribution links

### Phase 2: Optimization (Week 2-3)
- [ ] A/B test share button placement
- [ ] Optimize landing page
- [ ] Add social proof elements
- [ ] Test different share formats

### Phase 3: Amplification (Week 4)
- [ ] Implement referral rewards
- [ ] Add "most shared" leaderboard
- [ ] Create sharing templates
- [ ] Launch sharing campaign

## Success Criteria
- K-factor > 0.5
- 100+ shares/week
- 20% view-to-try conversion
- 500 new users/month from viral

## Risks & Mitigation
| Risk | Mitigation |
|------|------------|
| Low share rate | Make outputs more impressive |
| Poor conversion | Optimize landing experience |
| Spam concerns | Rate limiting, quality checks |
EOF
        ;;
    content)
        cat > "$DESIGN_FILE" << EOF
# Growth Loop Design: Content Loop for ${SKILL_NAME}

**Type**: Content  
**Skill**: ${SKILL_NAME}  
**Designed**: $(date -u +%Y-%m-%dT%H:%M:%SZ)

## Loop Diagram

\`\`\`
[User] → [Use ${SKILL_NAME}] → [Publish Output] → [Index by Search]
                                           ↓
[New User] ← [Search Discovery] ←── [View Content] ←── [Rank]
\`\`\`

## Components

### Input: User Creates Content
- **Source**: Skill outputs
- **Format**: Public pages, templates, examples
- **SEO**: Optimized for relevant keywords

### Action: Publish
- **Default**: Public (opt-out)
- **Indexing**: Automatic SEO optimization
- **Distribution**: Search engines, skill directory

### Output: Discoverable Content
- **Format**: Gallery, examples, templates
- **SEO**: Rich snippets, meta tags
- **Freshness**: Regular updates

### Conversion: Search → Use
- **Discovery**: Organic search traffic
- **Landing**: Contextual entry points
- **Target Rate**: 10%

### Amplification
- **SEO**: Content quality, backlinks
- **Freshness**: Regular new content
- **Authority**: Domain expertise

## Metrics

| Metric | Target |
|--------|--------|
| Content Velocity | 20 items/week |
| Organic Traffic | 1000 visits/month |
| Search Conversion | 10% |
| Content Quality Score | > 8/10 |

## Implementation Plan

### Phase 1: Content Foundation
- [ ] Make outputs public by default
- [ ] Add SEO metadata
- [ ] Create content gallery
- [ ] Submit to search engines

### Phase 2: Quality & Discovery
- [ ] Optimize for keywords
- [ ] Add rich snippets
- [ ] Build backlinks
- [ ] Create featured examples

### Phase 3: Scale
- [ ] Content partnerships
- [ ] User-generated content
- [ ] Template marketplace
- [ ] API for integrations

## Success Criteria
- 1000+ indexed pages
- 1000+ organic visits/month
- 10% search-to-use conversion
- Top 3 rankings for key terms
EOF
        ;;
    network)
        cat > "$DESIGN_FILE" << EOF
# Growth Loop Design: Network Loop for ${SKILL_NAME}

**Type**: Network  
**Skill**: ${SKILL_NAME}  
**Designed**: $(date -u +%Y-%m-%dT%H:%M:%SZ)

## Loop Diagram

\`\`\`
[User Joins] → [Invite Others] → [Collaborate] → [More Value]
      ↑                                              ↓
      └────────────── [Network Grows] ←──────────────┘
\`\`\`

## Components

### Input: User Joins
- **Onboarding**: Personal or team
- **Activation**: First use experience
- **Context**: Individual or organization

### Action: Invite & Collaborate
- **Invite**: Easy team invites
- **Collaborate**: Shared workspaces
- **Value**: Better together

### Output: Network Value
- **More Users**: More content, insights
- **More Content**: More value for all
- **Network Effects**: Value ∝ Users²

### Conversion: Invite → Join
- **Mechanism**: Team invites, sharing
- **Incentive**: Collaborative features
- **Target Rate**: 30%

### Amplification
- **Team Features**: Shared projects
- **Organization**: Enterprise features
- **Viral**: Team invites

## Metrics

| Metric | Target |
|--------|--------|
| Invites/User | 3 |
| Invite Acceptance | 30% |
| Team Retention | 60% |
| Network Density | 0.4 |

## Implementation Plan

### Phase 1: Collaboration
- [ ] Team workspaces
- [ ] Shared projects
- [ ] Comments & feedback
- [ ] Activity feeds

### Phase 2: Growth
- [ ] Invite system
- [ ] Team onboarding
- [ ] Organization features
- [ ] Admin controls

### Phase 3: Network Effects
- [ ] Public galleries
- [ ] Community features
- [ ] Integrations
- [ ] Marketplace

## Success Criteria
- 3 invites per active user
- 30% invite acceptance
- 60% team retention
- Clear network effects
EOF
        ;;
    engagement)
        cat > "$DESIGN_FILE" << EOF
# Growth Loop Design: Engagement Loop for ${SKILL_NAME}

**Type**: Engagement  
**Skill**: ${SKILL_NAME}  
**Designed**: $(date -u +%Y-%m-%dT%H:%M:%SZ)

## Loop Diagram

\`\`\`
[Use Skill] → [Complete Task] → [Earn Reward] → [Build Habit]
      ↑                                              ↓
      └────────────── [Daily Use] ←──────────────────┘
\`\`\`

## Components

### Input: Use Skill
- **Trigger**: Need or habit
- **Context**: Daily workflow
- **Friction**: Low

### Action: Complete & Reward
- **Completion**: Task finished
- **Reward**: Points, badges, progress
- **Feedback**: Immediate

### Output: Habit Formation
- **Streaks**: Daily usage
- **Progress**: Visible advancement
- **Mastery**: Skill improvement

### Conversion: Reward → Repeat
- **Mechanism**: Intrinsic + extrinsic motivation
- **Timing**: Immediate feedback
- **Target**: Daily habit

### Amplification
- **Streaks**: Don't break the chain
- **Levels**: Progression system
- **Social**: Leaderboards, sharing

## Metrics

| Metric | Target |
|--------|--------|
| Daily Active Users | 40% of total |
| Session Frequency | 5x/week |
| Streak Retention | 30% at 7 days |
| Habit Formation | 50% at 30 days |

## Implementation Plan

### Phase 1: Rewards
- [ ] Point system
- [ ] Achievement badges
- [ ] Progress bars
- [ ] Completion celebrations

### Phase 2: Habits
- [ ] Streak tracking
- [ ] Daily goals
- [ ] Reminders
- [ ] Habit stats

### Phase 3: Community
- [ ] Leaderboards
- [ ] Challenges
- [ ] Social sharing
- [ ] Competitions

## Success Criteria
- 40% DAU/MAU ratio
- Average 5 sessions/week
- 30% 7-day streak retention
- 50% habit formation at 30 days
EOF
        ;;
esac

echo -e "${GREEN}✅ Growth loop design complete${NC}"
echo -e "${BLUE}📄 Design saved: $DESIGN_FILE${NC}"
