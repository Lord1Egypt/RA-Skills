import TimeInput from "/assets/v3/components/time_input.js"

export default {
components:{
    "time-input":TimeInput
},
inject:['service', 'tags'],
data() {return {
    outsideAddr:'',
    backup:{
        at:-1,
        atObj:'',
        recent:'',
        balance:0,
        buckets:[] //id list
    },
    addrList:[],
    cmds:{backup:false,restore:false,setbackup:false},
    bucketOpts:[]//[{label:'xxx',value:123}...]
}},
created(){
    this.init();
    this.service.supportedCmds().then(list=> {
        this.cmds.backup=findInArray(list,'backup')>=0;
        this.cmds.restore=findInArray(list,'restore')>=0;
        this.cmds.setbackup=findInArray(list,'setbackup')>=0;
    });
},
methods:{
init() {
    this.getBackup();

    //从云侧查询bucket列表
    this.service.request_cloud({method:"GET",url:"/oss/allbuckets"},"company").then(resp => {
        if(resp.code != RetCode.OK) {
            this.bucketOpts=[];
            return;
        }
        var opts=[];
        for(var b of resp.data.buckets) {
            opts.push({label:b.city,value:''+b.id});
        }
        this.bucketOpts=opts;
    })
},
getBackup() {
    this.service.request_cloud({method:"GET",url:"/webdb/getBackupAt"}, "company").then(resp=>{
        if(resp.code!=RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        var info=resp.data;
        if(!info.recent || info.recent<=0) {
            this.backup.recent=this.tags.neverBackup;
        } else {
            this.backup.recent=datetime2str(new Date(info.recent));
        }
        this.backup.at=info.backupAt;
        if(info.backupAt >= 0) {
            var at = info.backupAt - (new Date()).getTimezoneOffset();
            if(at < 0) { //转成UTC
                at += 1440;
            } else if(at >= 1440) {
                at -= 1440;
            }
            var h=parseInt(at / 60);
            var m=parseInt(at % 60);
            this.backup.atObj=(h<10 ? ('0'+h) : (''+h))+ ':' + (m<10 ? ('0'+m) : (''+m));
        } else {
            this.backup.atObj='';
        }
    });

    //从云侧获取已选中的bucket
    this.service.request_cloud({method:"GET",url:"/service/getinfo?service=backup"},"company").then(resp => {
        if(resp.code != RetCode.OK) return;
        this.backup.balance=resp.data.balance;
        this.backup.buckets=resp.data.ext.split(',');
    }) 
},
switchBackup() {
    if(this.backup.at<0) {
        var at=120+(new Date()).getTimezoneOffset(); //默认凌晨2点
        if(at < 0) { //转成UTC
            at += 1440;
        } else if(at >= 1440) {
            at -= 1440;
        }
        this.backup.at=at;
        this.backup.atObj='02:00';
        this.turnOn('backup');
    } else {
        this.backup.at=-1;
        this.backup.atObj='';
        if(this.backup.balance<=0) {
            this.turnOff('backup');
        }
    }
    this.saveBackupAt();
},
turnOn(service) {
    var opts={method:"PUT",url:"/api/service/turnon", data:{service:service}};
    //只是在服务侧登记服务，并没有充值
    this.service.request_cloud(opts,"company").then(resp => {
        if(resp.code != RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
        }
    })
},
turnOff(service) {
    var opts={method:"DELETE",url:"/api/service/turnoff?service="+service};
    this.service.request_cloud(opts,"company").then(resp => {
        if(resp.code != RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
        }
    })
},
bucketChanged() {
    var buckets='';
    for(var b of this.backup.buckets) { //转为字符串
        if(buckets!='') buckets += ',';
        if(b!='') buckets += b;
    }
    if(buckets.length==0) {
        this.$refs.alertDlg.show(this.tags.needBuckets);
        return;
    }
    var opts={method:"PUT",url:"/api/oss/setmybuckets",
        data:{service:'backup',buckets:buckets}};
    this.service.request_cloud(opts, 'company').then(resp => {
        if(resp.code != RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
        }
    });
},
backupAtChanged(v) {
    if(this.backup.at<0)return;//尚未从服务器查询到时，不必保存，因为刚进页面时，会触发设置为当前时间
    this.backup.at=v.details.minute + v.details.hour*60;
    this.saveBackupAt();
},
saveBackupAt() {
    var at = this.backup.at;
    if(at>=0) {
        at += (new Date()).getTimezoneOffset();
        if(at < 0) { //转成UTC，在端侧才有效
            at += 1440;
        } else if(at >= 1440) {
            at -= 1440;
        }
    }
    this.service.command({cmd:'setBackup', at:at}).then(resp => {
        if(resp.code != RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
        }
    });
},
backupNow() {
    this.$refs.procDlg.show(this.tags.cfg.backup,
        this.tags.backupAlert, 'backup',
        (dlg)=> {
            dlg.setInfo('');
            return this.service.command({cmd:"backup"}, 100000);
        },
        (dlg,resp)=> {
          if(resp.code!=RetCode.OK) {
            dlg.setInfo(formatErr(resp.code, resp.info));
          } else {
            dlg.setInfo(this.tags.backupSuccess);
          }
        }
    )
},
restore() {
    this.$refs.procDlg.show(this.tags.cfg.restore,
        this.tags.restoreAlert, 'cloud_download',
        (dlg)=> {
            dlg.setInfo('');
            return this.service.command({cmd:"restore"}, 100000);
        },
        (dlg,resp)=> {
          if(resp.code!=RetCode.OK) {
            dlg.setInfo(formatErr(resp.code, resp.info));
          } else {
            dlg.setInfo(this.tags.restoreSuccess);
          }
        }
    )
}
},
template: `
<q-layout view="hHh lpr fFf">
<q-header class="bg-grey-1 text-primary">
 <q-toolbar>
  <q-btn icon="arrow_back" dense @click="service.go_back" flat round></q-btn>
  <q-toolbar-title>{{tags.cfg.backup}}</q-toolbar-title>
  <q-btn icon="power_settings_new" :label="backup.at<0?tags.startup:tags.shutdown"
    @click="switchBackup" dense flat v-if="cmds.setbackup" rounded color="primary"></q-btn>
 </q-toolbar>
</q-header>
<q-page-container>
 <q-page>
<q-markup-table bordered="false" flat>
 <tr>
  <td>{{tags.cfg.recentBackup}}</td>
  <td>{{backup.recent}}</td>
 </tr>
 <tr v-if="cmds.backup">
  <td>
   <q-btn flat icon="cloud_download" :label="tags.cfg.restore"
    @click="restore" color="primary" dense class="q-ml-md"
    :disable="backup.at<0"></q-btn>
  </td><td>
   <q-btn outline icon="backup" :label="tags.cfg.backupNow"
    @click="backupNow" color="primary" dense
    :disable="backup.at<0"></q-btn>
  </td>
 </tr>
 <tr>
  <td>{{tags.cfg.backupAt}}</td>
  <td>
   <time-input v-model.number="backup.atObj" :showSecond="false"
    @update:model-value="backupAtChanged"
    :disable="backup.at<0" type="number"></time-input>
  </td>
 </tr>
 <tr>
  <td>{{tags.cfg.buckets}}</td>
  <td>
   <q-option-group type="checkbox" :options="bucketOpts" v-model="backup.buckets"
   @update:model-value="bucketChanged" :disable="backup.at<0"></q-option-group>
  </td>
 </tr>
</q-markup-table>

 </q-page>
</q-page-container>
</q-layout>

<component-process-dialog ref="procDlg"></component-process-dialog>
<component-alert-dialog :title="tags.alert" :errMsgs="tags.errMsgs" ref="alertDlg"></component-alert-dialog>
`
}