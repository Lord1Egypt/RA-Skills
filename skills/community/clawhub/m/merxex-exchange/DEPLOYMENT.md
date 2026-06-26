# ZeroClaw Website - AWS Deployment Guide

## Overview
This guide walks you through deploying the ZeroClaw website to AWS using S3 + CloudFront for a fast, secure, and scalable hosting solution.

## Prerequisites
- AWS Account
- Domain name (optional, but recommended)
- SSL certificate (AWS will provide via CloudFront)

## Deployment Steps

### 1. Create S3 Bucket

```bash
# Create bucket (replace region as needed)
aws s3 mb s3://zeroclaw-website --region us-east-1

# Configure bucket for static website hosting
aws s3 website s3://zeroclaw-website \
    --index-document index.html \
    --error-document index.html
```

### 2. Upload Website Files

```bash
# Upload all files
aws s3 sync /home/ubuntu/.zeroclaw/workspace/zeroclaw-website/ \
    s3://zeroclaw-website \
    --region us-east-1

# Set CORS policy (if needed for API calls)
cat > cors-config.json <<EOF
{
    "CORSRules": [
        {
            "AllowedHeaders": ["*"],
            "AllowedMethods": ["GET"],
            "AllowedOrigins": ["*"],
            "MaxAgeSeconds": 3000
        }
    ]
}
EOF

aws s3api put-bucket-cors \
    --bucket zeroclaw-website \
    --cors-configuration file://cors-config.json
```

### 3. Create CloudFront Distribution

```bash
# Create CloudFront distribution config
cat > cloudfront-config.json <<EOF
{
    "CallerReference": "zeroclaw-website-$(date +%s)",
    "Origins": {
        "Quantity": 1,
        "Items": [
            {
                "Id": "zeroclaw-origin",
                "DomainName": "zeroclaw-website.s3.amazonaws.com",
                "S3OriginConfig": {
                    "OriginPath": "",
                    "OriginAccessIdentity": ""
                }
            }
        ]
    },
    "DefaultCacheBehavior": {
        "TargetOriginId": "zeroclaw-origin",
        "ViewerProtocolPolicy": "redirect-to-https",
        "AllowedMethods": {
            "Quantity": 3,
            "Items": ["GET", "HEAD", "OPTIONS"],
            "CachedMethods": {
                "Quantity": 2,
                "Items": ["GET", "HEAD"]
            }
        },
        "TrustedSigners": {
            "Enabled": false,
            "Quantity": 0
        },
        "ForwardedValues": {
            "QueryString": false,
            "Cookies": {
                "Forward": "none"
            }
        },
        "MinTTL": 0,
        "DefaultTTL": 86400,
        "MaxTTL": 31536000
    },
    "Comment": "ZeroClaw Website Distribution",
    "Enabled": true
}
EOF

# Create distribution
aws cloudfront create-distribution --distribution-config file://cloudfront-config.json
```

### 4. Configure Custom Domain (Optional)

```bash
# Request SSL certificate in us-east-1
aws acm request-certificate \
    --domain-name yourdomain.com \
    --validation-method DNS \
    --region us-east-1

# After DNS validation, associate certificate with CloudFront
# (Use AWS Console or update distribution with certificate ARN)
```

### 5. Set Up DNS

Add these records to your domain's DNS:

```
Type: A
Name: @
Value: <CloudFront Distribution Domain>

Type: CNAME
Name: www
Value: <CloudFront Distribution Domain>
```

## Cost Optimization

- **S3**: ~$0.023/GB/month + request costs
- **CloudFront**: ~$0.085/GB for first 10TB
- **Estimated monthly cost**: $5-20 for moderate traffic

Enable CloudFront caching and S3 lifecycle policies for cost savings.

## Monitoring

1. **CloudWatch Metrics**: Monitor requests, errors, latency
2. **S3 Analytics**: Track access patterns
3. **CloudFront Logs**: Enable access logging to S3

## Security Checklist

- [ ] SSL/TLS enabled (CloudFront default)
- [ ] HTTPS enforced (ViewerProtocolPolicy: redirect-to-https)
- [ ] S3 bucket private (no direct access)
- [ ] CloudFront OAI/OAC configured
- [ ] WAF rules (optional, for DDoS protection)
- [ ] CORS configured minimally

## Environment Variables

Create `.env` for any configuration:

```bash
AWS_REGION=us-east-1
S3_BUCKET=zeroclaw-website
CLOUDFRONT_DOMAIN=<your-cloudfront-url.com>
STRIPE_PUBLIC_KEY=pk_live_...
```

## Post-Deployment Testing

```bash
# Test HTTPS
curl -I https://your-domain.com

# Test redirect
curl -I http://your-domain.com

# Check CloudFront status
aws cloudfront get-distribution --id <distribution-id>
```

## Updates

To update the website:

```bash
# Update S3
aws s3 sync /home/ubuntu/.zeroclaw/workspace/zeroclaw-website/ \
    s3://zeroclaw-website

# Invalidate CloudFront cache (if needed)
aws cloudfront create-invalidation \
    --distribution-id <distribution-id> \
    --paths "/*"
```

## Stripe Integration

See `stripe-integration.md` for payment processing setup.

---

**Deployment Complete!** 🦀

Your ZeroClaw website is now live and ready to attract clients.