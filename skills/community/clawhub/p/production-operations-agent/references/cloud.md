# Cloud Infrastructure Investigation Reference

Load this when the incident involves AWS, GCP, or Azure resources — cost spikes, networking, managed services, IAM, or regional issues.

## Key Signals to Surface

- Cost anomalies: unexpected spend on EC2, RDS, data transfer, S3, or Lambda
- Networking: VPC routing, security group changes, NAT gateway exhaustion
- IAM: permission denied errors, newly modified roles/policies
- Managed services: RDS failover, ElastiCache evictions, SQS backlog, Kinesis throttling
- Regional/AZ: availability zone degradation, service health dashboard events

## Suggested `neubird investigate` Prompts

```
"AWS costs spiked overnight — identify the service and root cause"
"EC2 instances in us-east-1a are unreachable — what changed?"
"RDS read replica is lagging by 2 hours — investigate"
"S3 bucket is returning 403s that weren't happening yesterday"
"Lambda function cold start latency doubled — why?"
```

## Cost Spike Investigation Checklist

1. Which service drove the spike (Cost Explorer by service)?
2. Was there a traffic increase, or did unit cost change?
3. Any new resources provisioned (look at CloudTrail)?
4. Data transfer costs — did something start egressing to internet?
5. Reserved capacity expired and fell back to on-demand?
