# Example Vulnerable Terraform Code

Terraform examples for you to copy into your own main.tf file to try using the Gomboc Community skill.

``` terraform
resource "aws_s3_bucket" "vulnerable_bucket" {
  bucket = "my-vulnerable-bucket"
}

# Issue: S3 bucket is not encrypted
# Fix: Enable server-side encryption

resource "aws_security_group" "insecure_sg" {
  name = "insecure-sg"

  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Issue: Allows all traffic
  }
}

# Fix: Restrict to specific CIDR blocks or security groups

resource "aws_db_instance" "vulnerable_db" {
  allocated_storage    = 20
  engine              = "mysql"
  engine_version      = "5.7"
  instance_class      = "db.t2.micro"
  name                = "mydb"
  username            = "admin"
  password            = "password123"  # Issue: Hardcoded password
  skip_final_snapshot = true
  publicly_accessible = true  # Issue: Exposed to internet
}

# Fix: Use secrets manager for password, set to false for publicly_accessible

resource "aws_iam_user" "vulnerable_user" {
  name = "legacy-user"
}

resource "aws_iam_access_key" "vulnerable_key" {
  user = aws_iam_user.vulnerable_user.name
}

# Issue: Long-lived access keys without rotation
# Fix: Use temporary credentials or enable key rotation

resource "aws_kms_key" "unencrypted" {
  description = "Unmanaged encryption"
  # Issue: No rotation policy
  # Fix: Enable key rotation
}
```