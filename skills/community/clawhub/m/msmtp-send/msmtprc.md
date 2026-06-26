# dnf install -y msmpt
# Fill out your details and place this file in ~/.msmtprc

defaults
auth            on
tls             on
tls_starttls    on
tls_trust_file  /etc/pki/tls/certs/ca-bundle.crt
account         gmail
host            smtp.gmail.com
port            587
from            user@gmail.com
user            user_account@gmail.com
password        abcd efgh ijkl mnop 	# Use the password from https://myaccount.google.com/apppasswords
					# You need to enable 2fa on your account to access the apppasswords
account default : gmail
