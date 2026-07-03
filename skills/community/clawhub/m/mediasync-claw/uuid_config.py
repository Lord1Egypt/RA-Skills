import configparser
import os
import uuid

class UUIDConfig:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uuid.ini")
    
    def get_uuid(self):
        uuid_value = self.query_uuid()
        if uuid_value is None:
            uuid_value = uuid.uuid4().hex
            self.update_uuid(uuid_value)
        
        return uuid_value

    def update_uuid(self, uuid):
        self.config['comm'] = {'uuid_value': uuid}
        with open(self.config_file_path, 'w') as configfile:
            self.config.write(configfile)

    def query_uuid(self):
        self.config.read(self.config_file_path)
        if 'comm' not in self.config or 'uuid_value' not in self.config['comm']:
            print("Error: UUID not found in config. Please run setup_uuid() first.")
            return None
        return self.config['comm']['uuid_value']